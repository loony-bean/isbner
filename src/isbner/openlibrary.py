# -*- coding: utf-8 -*-

from adaptor import Adaptor
from utils import fetch

try:
    from django.utils import simplejson
except ImportError:
    import simplejson

class OpenLibrary(Adaptor):
    def __init__(self):
        self._name = 'OpenLibrary'
        self._url = 'http://openlibrary.org/'
        self._weight = 50

    def _run(self, isbn):
        url = 'http://openlibrary.org/api/books?bibkeys=ISBN:%s&jscmd=data&format=json' % isbn

        try:
            json = simplejson.loads(fetch(url))
            result = dict()
            json = json['ISBN:'+isbn]
            result['title'] = json['title']
            result['author'] = ', '.join([i['name'] for i in json['authors']])
            result['isbn'] = isbn
            result['publisher'] = ', '.join([i['name'] for i in json['publishers']])
            result['date'] = json['publish_date']
            result['source'] = json['url']
            return result
        except:
            return None

    def check(self):
        return self._run('0201558025') == {
            'title': u'Concrete mathematics',
            'author': u'Ronald L. Graham, Donald Knuth, Oren Patashnik',
            'isbn': u'0201558025',
            'publisher': u'Addison-Wesley',
            'date': u'1994',
            'source': u'http://openlibrary.org/books/OL1429049M/Concrete_mathematics'}

if __name__ == '__main__':
    print OpenLibrary().check()
