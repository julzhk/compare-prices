from itertools import *
import os
import pickle
import random

import jinja2
import webapp2
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required

from models import Product, Site, Page, ArchivePrice, Credentials
from oauth2client.appengine import StorageByKeyName
from oauth2client.client import OAuth2WebServerFlow


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Init(webapp2.RequestHandler):
    """
        Simple wipe & re-initialize the datastore with some testing data.
        Obviously, this will be deleted in the live site.
    """

    def get(self):
        for m in [Page, Site, Product, ArchivePrice]:
            for i in m.query():
                i.key.delete()
        self.response.out.write('ok, nuked')
        t = Site(
            name='acme.com',
            price_class='acme',
            url='http://www.acme.com'
        )
        t.put()
        for name, url in [
            ('Product A', 'http://www.example.com?id=1'),
            ('Product B', 'http://www.example.com?id=2'),
            ('Product C', 'http://www.example.com?id=3')
        ]:
            newproduct = Product(
                name=name,
                our_price=20 + random.random(),
                sku=name
            )
            newproduct.put()
            page = Page(url=url,
                        product=newproduct.key,
                        site=t.key,
                        current_price=99.9)
            page.put()
        t = Site(
            name='betta stuff',
            price_class='betta_stuff',
            url='http://betta_stuff.example.com'
        )
        t.put()
        for name, url in [
            ('Product A', 'http://betta_stuff.example.com?id=5'),
            ('Product B', 'http://betta_stuff.example.com?id=6'),
            ('Product D', 'http://betta_stuff.example.com?id=9')
        ]:
            newproduct = Product(name=name, our_price=20 + random.random(), sku=name)
            newproduct.put()
            page = Page(url=url,
                        product=newproduct.key,
                        site=t.key,
                        current_price=99.9)
            page.put()


class Update(webapp2.RequestHandler):
    """
        Called by the google app engine CRON
    """

    @staticmethod
    def store_archive(page):
        """
            On any price Update simply put the old data into Archive store.
        """
        site = Site.query(Site.key == page.site).get()
        a = ArchivePrice(
            product=page.product,
            date=page.date,
            price=page.current_price,
            url=page.url,
            site=site.name
        )
        a.put()

    def get(self):
        """
            Update all the prices, using the 'price_class' model's beautiful
            soup  to scrape
        """
        allpages = Page.query().order(Page.date).fetch()
        for page in allpages:
            site = Site.query(Site.key == page.site).get()
            g = eval(site.price_class)()
            page.current_price = g.get_price(url=page.url)
            self.store_archive(page)
            page.put()
        self.response.out.write('pages scraped and updated')


class Archive(webapp2.RequestHandler):
    """
        Show the Archive: just a list currently (chart to follow)
    """

    def get(self):
        k = self.request.get('product')
        get_product = Product.get_by_id(int(k))
        archive_data = ArchivePrice.query(ArchivePrice.product == get_product.key).fetch()
        template_values = {
            'product': get_product,
            'data': archive_data,
        }
        template = jinja_environment.get_template('templates/Archive.html')
        self.response.out.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):
    @staticmethod
    def grouper(data):
        data.sort()
        r = []
        for product_key, outer_grouper in groupby(data, lambda o: o.product):
            p = Product.query(Product.key == product_key).get()
            for site_name, inner_grouper in groupby(list(outer_grouper), lambda o: o.url):
                for page in inner_grouper:
                    page.product_data = p
                    s = Site.query(Site.key == page.site).get()
                    page.site_name = s.name
                    r.append(page)
        r = sorted(r, key=lambda prod: prod.product_data.name)
        return r

    @login_required
    def get(self):
        user = users.get_current_user()
        credentials = StorageByKeyName(Credentials, user.user_id(), 'credentials').get()
        if self.request.get('logout'):
            if credentials:
                StorageByKeyName(Credentials, user.user_id(), 'credentials').locked_delete()
            self.response.out.write('Thanks, you are now logged out')
            return
        if credentials:
            allproducts = Product.query().fetch()
            allpages = Page.query().order(Page.product).fetch()
            product_list = self.grouper(data=allpages)
            template_values = {
                'products': allproducts,
                'pages': product_list,
                'user_email': user.email()
            }

            template = jinja_environment.get_template('templates/main.html')
            self.response.out.write(template.render(template_values))
        else:
            flow = OAuth2WebServerFlow(
                client_id='<myid>.apps.googleusercontent.com',
                client_secret='<secret>',
                scope='https://www.googleapis.com/auth/buzz',
                user_agent='comparinator')
            callback = 'http://comparinator.appspot.com/oauth2callback'
            authorize_url = flow.step1_get_authorize_url(redirect_uri=callback)
            memcache.set(user.user_id(), pickle.dumps(flow))
            self.redirect(authorize_url)
            return


class OAuthHandler(webapp.RequestHandler):
    @login_required
    def get(self):
        user = users.get_current_user()
        flow = pickle.loads(memcache.get(user.user_id()))
        if flow:
            credentials = flow.step2_exchange(self.request.params)
            StorageByKeyName(Credentials, user.user_id(), 'credentials').put(credentials)
            self.redirect('/')
        else:
            self.response.out.write('no flow')


app = webapp2.WSGIApplication([
                                  ('/Init', Init),
                                  ('/get', Update),
                                  ('/Archive', Archive),
                                  ('/oauth2callback', OAuthHandler),
                                  ('/', MainPage),
                              ], debug=True)