# -*- coding: utf-8 -*-

from utils import sanitize 

class Adaptor(object):
    def __init__(self):
        self._name = 'Default'
        self._url = 'http://www.example.com/'
        self._weight = 0

    def _run(self, isbn):
        return None

    def check(self):
        return False

    def dump(self, isbn):
        data = self._run(isbn)
        if data is not None:
            data = {
                'fields': dict(zip(data.keys(), 
                                   map(lambda i: (i, self._weight), 
                                       data.values()))),
                'sources': {self._name: data['source']}
                }
            del data['fields']['source']
        else:
            data = {'fields': {}, 'sources': {}}
        data['providers'] = [self._name]
        return data

    name = property(fget=lambda self: self._name)
    url = property(fget=lambda self: self._url)
    weight = property(fget=lambda self: self._weight)
