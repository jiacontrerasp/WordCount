import logging
import urllib
import re
from google.appengine.ext import deferred
from google.appengine.api import memcache



def read_web_site(url, deep, words, visited = list()):
    deep -= 1
    visited.append(url)
    increment_links(1)
    logging.info("Searching for links in %s", url)
    if deep >= 0:
        req = urllib.urlopen(url)
        encoding=req.headers['content-type'].split('charset=')[-1]
        html = unicode(req.read(),encoding)
        for word in words.split(','):
            word_count = html.count(word)
            if word_count:
                increment_word(word_count, word)

        for link in find_links(html):
            if link.startswith('http') and link not in visited:
                deferred.defer(read_web_site, link, deep, words, visited)
    else:
        pass

def find_links(html):
    return re.findall(r'href=[\'"]?([^\'" >]+)', html)

def increment_links(number):
    memcache.incr("links", delta=number, initial_value=0)

def increment_word(number,word):
    memcache.incr("word-%s" % word, delta=number, initial_value=0)
