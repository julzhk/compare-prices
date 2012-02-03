= Introduction =

  >>> from bs4 import BeautifulSoup
  >>> soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
  >>> print soup.prettify()
  <html>
   <body>
    <p>
     Some
     <b>
      bad
      <i>
       HTML
      </i>
     </b>
    </p>
   </body>
  </html>
  >>> soup.find(text="bad")
  u'bad'

  >>> soup.i
  <i>HTML</i>

  >>> soup = BeautifulSoup("<tag1>Some<tag2/>bad<tag3>XML", "xml")
  >>> print soup.prettify()
  <?xml version="1.0" encoding="utf-8">
  <tag1>
   Some
   <tag2 />
   bad
   <tag3>
    XML
   </tag3>
  </tag1>

= About Beautiful Soup 4 =

This is a nearly-complete rewrite that removes Beautiful Soup's custom
HTML parser in favor of a system that lets you write a little glue
code and plug in any HTML or XML parser you want.

Beautiful Soup 4.0 comes with glue code for four parsers:

 * Python's standard HTMLParser (html.parser in Python 3)
 * lxml's HTML and XML parsers
 * html5lib's HTML parser

HTMLParser is the default, but I recommend you install one of the
other parsers, or you'll have problems handling real-world markup.

For complete documentation, see the Sphinx documentation in
docs/source. What follows is a summary of the changes from Beautiful
Soup 3.

== The module name has changed ==

Previously you imported the BeautifulSoup class from a module also
called BeautifulSoup. To save keystrokes and make it clear which
version of the API is in use, the module is now called 'bs4':

    >>> from bs4 import BeautifulSoup

== It works with Python 3 ==

Beautiful Soup 3.1.0 worked with Python 3, but the parser it used was
so bad that it barely worked at all. Beautiful Soup 4 works with
Python 3, and since its parser is pluggable, you don't sacrifice
quality.

Special thanks to Thomas Kluyver and Ezio Melotti for getting Python 3
support to the finish line. Ezio Melotti is also to thank for greatly
improving the HTML parser that comes with Python 3.2.

== CDATA sections are normal text, if they're understood at all. ==

Currently, the lxml and html5lib HTML parsers ignore CDATA sections in
markup:

 <p><![CDATA[foo]]></p> => <p></p>

A future version of html5lib will turn CDATA sections into text nodes,
but only within tags like <svg> and <math>:

 <svg><![CDATA[foo]]></svg> => <p>foo</p>

The default XML parser (which uses lxml behind the scenes) turns CDATA
sections into ordinary text elements:

 <p><![CDATA[foo]]></p> => <p>foo</p>

In theory it's possible to preserve the CDATA sections when using the
XML parser, but I don't see how to get it to work in practice.

== Miscellaneous other stuff ==

If the BeautifulSoup instance has .is_xml set to True, an appropriate
XML declaration will be emitted when the tree is transformed into a
string:

    <?xml version="1.0" encoding="utf-8">
    <markup>
     ...
    </markup>

The ['lxml', 'xml'] tree builder sets .is_xml to True; the other tree
builders set it to False. If you want to parse XHTML with an HTML
parser, you can set it manually.

= Running the unit tests =

Here's how to run the tests on Python 2.7:

 $ cd bs4
 $ python2.7 -m unittest discover -s bs4

Here's how to do it with Python 3.2:

 $ ./convert-py3k
 $ cd py3k/bs4
 $ python3 -m unittest discover -s bs4

The script test-all-versions will run the tests twice, once on Python
2.7 and once on Python 3.
