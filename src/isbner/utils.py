# -*- coding: utf-8 -*-

try:
    from google.appengine.api.urlfetch import fetch
except ImportError:
    from urllib import urlopen
    def fetch(url):
        try:
            return urlopen(url).read()
        except:
            return ""

def sanitize(isbn):
    """
    >>> sanitize('020-155 80 25')
    0201558025
    """
    return filter(str.isalnum, isbn)

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
