from google.appengine.ext.ndb import model
from BeautifulSoup import BeautifulSoup
import re

class Product(model.Model):
    name = model.StringProperty()
    sku = model.StringProperty()
    our_price = model.FloatProperty()
    our_url = model.FloatProperty()

class Site(model.Model):
    name = model.StringProperty(indexed=True)
    price_class = model.StringProperty()
    url = model.StringProperty()


class Page(model.Expando):
    url = model.StringProperty(indexed=True)
    site = model.KeyProperty()
    product = model.KeyProperty()
    date = model.DateTimeProperty(auto_now_add=True)
    current_price = model.FloatProperty()

class Archive_Price(model.Model):
    product = model.KeyProperty()
    date = model.DateTimeProperty()
    price = model.FloatProperty()
    url = model.StringProperty()
    site = model.StringProperty()



class retailer(object):
    def get_page_content(self,url):
        from google.appengine.api import urlfetch
        result = urlfetch.fetch(url=url)
        if result.status_code == 200:
            return result.content


class greenfingers(retailer):
    def get_price(self,url):
        html_doc  = self.get_page_content(url =url)
        soup = BeautifulSoup(html_doc)
        for i in soup.findAll(color="#f0d637"):
            for c in i.contents:
                price = re.findall(r'[0-9\.]+', str(c))
                if price:
                    return float(price[0])


class gardenforless(retailer):
    def get_price(self,url):
        html_doc  = self.get_page_content(url =url)
        soup = BeautifulSoup(html_doc)
        i = soup.find(id="pricediv0")
        c = i.contents[0]
        price = re.findall(r'[0-9\.]+', c)
        if price:
            return float(price[0])
