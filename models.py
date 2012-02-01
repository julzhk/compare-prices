from google.appengine.ext.ndb import model

class Greeting(model.Model):
    content = model.StringProperty()
    date = model.DateTimeProperty(auto_now_add=True)