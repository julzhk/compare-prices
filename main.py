import webapp2
#from webapp2_extras import jinja2
import jinja2
import os
import random
from itertools import *
from operator import itemgetter
import pprint


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
from google.appengine.api import users
from models import *

class init(webapp2.RequestHandler):
    def get(self):
        for m in [Page,Site, Product]:
            print '*'*8, m
            for i in m.query():
                i.key.delete()
        print 'ok, nuked'
        t = Site(name = 'ebay', url = 'ebay')
        t.put()
        t2 = Site(name = 'amazon', url = 'amazon')
        t2.put()
        for name in ['bbq1','bbq 2','bbq3']:
            p = Product(name = name,our_price = 20+ random.random(),sku = name)
            p.put()
            page = Page(url = 'amazon.com',
                        product = p.key,
                        site = t.key,
                        current_price = 23.3+ random.random())
            page.put()
            page = Page(url = 'ebay.com',
                        site = t2.key,
                        product = p.key,
                        current_price = 15+ random.random())
            page.put()


class urlfetch(webapp2.RequestHandler):
    def get(self):
        from bs4 import BeautifulSoup, SoupStrainer
        from google.appengine.api import urlfetch
        result = urlfetch.fetch(url="http://www.example.com/")
        if result.status_code == 200:
            self.response.out.write('ok 200')
            self.response.out.write(result.content)
        self.response.out.write('LINKS')
        response = result.content
        for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
            if link.has_key('href'):
                self.response.out.write(link['href'])
                self.response.out.write('<br>')
        self.response.out.write('.. and out')

class MainPage(webapp2.RequestHandler):
    def grouper(self,data):
        data.sort()
        r = []
        for product_key, outer_grouper in groupby(data, lambda o:o.product):
            p = Product.query(Product.key== product_key).get()
            for site_name, inner_grouper in groupby(list(outer_grouper), lambda o:o.url):
                for page in inner_grouper:
                    page.product_data = p
                    s = Site.query(Site.key == page.site).get()
                    page.site_name = s.name
                    r.append(page)
        r = sorted(r, key=lambda p: p.product_data.name)
        return r

    def get(self):
        allproducts = Product.query().fetch()
        allpages = Page.query().order(Page.product).fetch()
        product_list = self.grouper(data=allpages)
        template_values = {
            'products':allproducts,
            'pages': product_list,
            }

        template = jinja_environment.get_template('templates/main.html')
        self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
        ('/init', init),
        ('/get', urlfetch),
        ('/', MainPage),
    ],debug=True)