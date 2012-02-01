import webapp2
#from webapp2_extras import jinja2
import jinja2
import os

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
from google.appengine.api import users
from models import Greeting

class MainPage(webapp2.RequestHandler):
    def get(self):
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

app = webapp2.WSGIApplication([('/', MainPage)],
                                               debug=True)