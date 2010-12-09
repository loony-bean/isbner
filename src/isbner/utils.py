# -*- coding: utf-8 -*-

from re import compile, sub
import pyisbn

NUMS = compile('\D')

def sanitize(isbn):
    """
    >>> sanitize('020-155 80 25')
    0201558025
    """
    return NUMS.sub('', str(isbn))

def isbn_validate(isbn):
    """
    >>> isbn_validate('9780262062792')
    False
    >>> isbn_validate('9780262062794')
    True
    """
    result = False
    try:
        if pyisbn.Isbn(isbn).validate():
            result = True
    except:
        pass
    return result

def isbn10(isbn):
    """
    >>> isbn10('9780671657130')
    '0671657135'
    """
    if len(isbn) == 13:
        isbn = pyisbn.convert(isbn)
    return isbn

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
            return {}
except ImportError:
    from urllib import urlopen
    def fetch(url):
        try:
            return urlopen(url).read()
        except:
            return ""
    def headers(url):
        try:
            headers = dict()
            info = urlopen(url).info()
            for i in info:
                headers[i] = info[i]
            return headers
        except:
            return {}

def content_length(url):
    hdrs = headers(url)
    if 'content-length' in headers:
        return int(headers['content-length'])
