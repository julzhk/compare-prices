Compare Prices: A Google App Engine Scraper
==============

This project was created for an e-commerce vendor to keep an eye on his competitors pricing by web scraping the prices page 
of certain key products regularly & creating an alert of any changes.

How it works
=====

The models.py file holds the definitions for each competitor retailer, and a 'get_price' method to extract (using beautiful soup)
the price on the page. Of course, if the competitor changes their site layout, these definitions will have to be updated.



