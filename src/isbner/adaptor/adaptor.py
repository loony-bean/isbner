# -*- coding: utf-8 -*-

class Adaptor(object):
    def __init__(self):
        self._name = "Default"
        self._weight = 0

    def run(self, isbn):
        return self.sort(self._run(isbn))

    def fetch(self, url):
        pass

    def check(self):
        return False

    def sort(self, data):
        order = frozenset('title',
                          'author',
                          'publisher',
                          'date',
                          'isbn')
        return data

    name = property(fget=lambda self: self._name)
    weight = property(fget=lambda self: self._weight)

try:
    from google.appengine.api.urlfetch import fetch

except ImportError:
    from urllib import urlopen

    def fetch(url):
        try:
            return urlopen(url).read()
        except:
            return ""
    
Adaptor.fetch = lambda self, url: fetch(url)
