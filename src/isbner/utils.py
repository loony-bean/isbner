# -*- coding: utf-8 -*-

from re import compile, sub
from pyisbn import Isbn

NUMS = compile('\D')

def sanitize(isbn):
    """
    >>> sanitize('020-155 80 25')
    0201558025
    >>> sanitize('9780262062792')
    False
    """
    try:
        num = Isbn(NUMS.sub('', str(isbn)))
        return num.isbn if num.validate() else False
    except:
        return False

def merge(dump, add):
    """
    >>> dump = {'fields': {'publisher': ('p1', 55), 'title': ('t1', 55)}, 'sources': {'s1': 'url1'}}
    >>> add = {'fields': {'publisher': ('p2', 50), 'date': ('d2', 50)}, 'sources': {'s2': 'url1'}}
    >>> merge(dump, add)
    {'fields': {'date': ('d2', 50), 'publisher': ('p1', 55), 'title': ('t1', 55)}, 'sources': {'s2': 'url2', 's1': 'url1'}}
    """
    merged = False
    for k in add['fields'].keys():
        if (k not in dump['fields']) or (dump['fields'][k][1] <
                                         add['fields'][k][1]):
            dump['fields'][k] = add['fields'][k]
            merged = True
    if merged:
        for k in add['sources'].keys():
            dump['sources'][k] = add['sources'][k]
    return dump

try:
    from google.appengine.api.urlfetch import fetch as urlfetch
    def fetch(url):
        try:
            return urlfetch(url).content
        except:
            return ""        
    def headers(url):
        try:
            return urlfetch(url).headers
        except:
            return dict()

except ImportError:
    from urllib import urlopen
    def fetch(url):
        try:
            return urlopen(url).read()
        except:
            return ""

    def headers(url):
        headers = dict()
        try:
            headers.update(urlopen(url).info())
        finally:
            return headers
