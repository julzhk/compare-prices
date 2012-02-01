import webapp2
#from webapp2_extras import jinja2
import jinja2
import os

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
from google.appengine.api import users
from models import *

class init(webapp2.RequestHandler):
    def get(self):
        for m in [Page,Site, Prodct, PriceInstance]:
            for i in m.query().fetch():
                i.delete()
        print 'ok, nuked'


class MainPage(webapp2.RequestHandler):
    def get(self):
        s = Site(url = 'example')
        s.put()
        p = Page(name = 'new page')
        p.site = s.key
        p.put()
        guestbook_name=self.request.get('guestbook_name', 'default')
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'guestbook_name': guestbook_name,
            'url': url,
            'url_linktext': url_linktext,
            }

        template = jinja_environment.get_template('templates/_base.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
        ('/init', init),
        ('/', MainPage),
    ],debug=True)