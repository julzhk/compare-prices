import webapp2
#from webapp2_extras import jinja2
import jinja2
import os

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
from google.appengine.api import users
from models import *

class init(webapp2.RequestHandler):
    def get(self):
        for m in [Page,Site, Product, PriceInstance]:
            print '*'*8, m
            for i in m.query():
                print i
                del(i)
        print 'ok, nuked'
        for name in ['bbq1','bbq2','bbq3']:
            p = Product(name = name)
            p.put()



class MainPage(webapp2.RequestHandler):
    def get(self):
        allproducts = Product.query()
        showproduct = self.request.get('product', '')



        template_values = {
            'products':allproducts,
            'showproduct':showproduct
            }

        template = jinja_environment.get_template('templates/main.html')
        self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
        ('/init', init),
        ('/', MainPage),
    ],debug=True)