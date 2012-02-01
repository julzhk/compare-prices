from google.appengine.ext.ndb import model

class Product(model.Model):
    name = model.StringProperty()
    sku = model.StringProperty()
    our_price = model.FloatProperty()
    our_url = model.FloatProperty()

class Site(model.Model):
    name = model.StringProperty(indexed=True)
    url = model.StringProperty()

class Page(model.Expando):
    url = model.StringProperty(indexed=True)
    site = model.KeyProperty()
    product = model.KeyProperty()
    price_xpath = model.KeyProperty()
    date = model.DateTimeProperty(auto_now_add=True)
    current_price = model.FloatProperty()
