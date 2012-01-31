from google.appengine.ext.ndb import model
import datetime

from google.appengine.ext.webapp import util
from ndb import model, context

class Greeting(model.Model):
    content = model.StringProperty()
    date = model.DateTimeProperty(auto_now_add=True)