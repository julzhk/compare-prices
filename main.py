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
        for name in ['bbq1','bbq 2','bbq3']:
            p = Product(name = name,our_price = 20+ random.random(),sku = name)
            p.put()
            page = Page(url = 'amazon.com',product = p.key,
                        current_price = 23.3+ random.random())
            page.put()
            page = Page(url = 'ebay.com',product = p.key,
                        current_price = 15+ random.random())
            page.put()


class MainPage(webapp2.RequestHandler):
    def grouper(self,data):
        data.sort()
        r = []
        print 'Grouped, sorted:'
        for k, g in groupby(data, lambda o:o.product):
#            print k
            p = Product.query(Product.key== k).get()
#            print p.name,':'
            for a, b in groupby(list(g), lambda o:o.url):
#                print a
                for c in b:
#                    print c.url, ' $ ',c.current_price
                    c.product_data = p
                    r.append(c)
        r = sorted(r, key=lambda p: p.product.urlsafe())
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
        ('/', MainPage),
    ],debug=True)