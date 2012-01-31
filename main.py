import webapp2
from google.appengine.api import users
from models import Greeting

class MainPage(webapp2.RequestHandler):
    def get(self):
        u = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')
        g = Greeting(content = 'hi')
        g.put()
        self.response.out.write(u)
        self.response.out.write(g.content)

app = webapp2.WSGIApplication([('/', MainPage)],
                                               debug=True)