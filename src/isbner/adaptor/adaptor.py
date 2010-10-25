# -*- coding: utf-8 -*-

class Adaptor(object):
    def __init__(self):
        self._name = "Default"
        self._weight = 0

    def _run(self, isbn):
        pass

    def run(self, isbn):
        return self.sort(self._run(isbn))

    def fetch(self, url):
        pass

    def check(self):
        return False

    def sort(self, data):
        fields = list('title',
                      'author',
                      'publisher',
                      'date',
                      'isbn',
                      'source')
        keys = fields + list(set(data.keys()) - set(fields))
        values = [data[k] for k in keys]
        keys = [k for k in keys]
        return (keys, values)

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
finally:
    Adaptor.fetch = lambda self, url: fetch(url)
