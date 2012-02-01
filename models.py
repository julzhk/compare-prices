from google.appengine.ext.ndb import model

class Product(model.Model):
    name = model.StringProperty()
    sku = model.StringProperty()
    our_price = model.StringProperty()
    our_url = model.StringProperty()

class Site(model.Model):
    name = model.StringProperty(indexed=True)
    url = model.StringProperty()

class Page(model.Model):
    url = model.StringProperty(indexed=True)
    site = model.KeyProperty()
    price_xpath = model.KeyProperty()

class PriceInstance(model.Model):
    date = model.DateTimeProperty(auto_now_add=True)
    page = model.KeyProperty
    price = model.FloatProperty()
