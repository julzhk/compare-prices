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
    def get_page_content(self,url):
        from google.appengine.api import urlfetch
        result = urlfetch.fetch(url=url)
        if result.status_code == 200:
            return result.content

    def get_price(self,url):
        html_doc  = self.get_page_content(url =url)
        from BeautifulSoup import BeautifulSoup
        import re
        soup = BeautifulSoup(html_doc)
        for i in soup.findAll(color="#f0d637"):
            for c in i.contents:
                price = re.findall(r'[0-9\.]+', str(c))
                if price:
                    return float(price[0])
    def get(self):
        for m in [Page,Site, Product]:
            print '*'*8, m
            for i in m.query():
                i.key.delete()
        self.response.out.write('ok, nuked')
        t = Site(name = 'greenfingers.com', url = 'http://www.greenfingers.com')
        t.put()
        for name in ['LS6157D Fire pit']:
            p = Product(name = name,our_price = 20+ random.random(),sku = name)
            p.put()
            url = 'http://www.greenfingers.com/superstore/product.asp?dept_id=2211&pf_id=LS6157D'
            page = Page(url =url,
                        product = p.key,
                        site = t.key,
                        current_price = self.get_price(url = url))
            page.put()


class urlfetch(webapp2.RequestHandler):


    def get(self):
        url = 'http://www.greenfingers.com/superstore/product.asp?dept_id=2211&pf_id=LS6157D'
#        s = self.get_page_content(url=url)
        s = self.get_price(url=url)
        self.response.out.write(s)

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