# -*- coding: utf-8 -*-

from adaptor import Adaptor
from utils import content_length
import pyisbn

class LibraryThing(Adaptor):
    def __init__(self):
        self._name = 'LibraryThing'
        self._url = 'http://www.librarything.com/'
        self._weight = 50

    def _run(self, isbn):
        try:
            # This dev key belongs to LibraryThing
            url = 'http://www.librarything.com/devkey/3f8ba261818a718f42e1c94df68f48b8/large/isbn/%s' % isbn
            if content_length(url) > 100:
                result = dict()
                result['isbn'] = isbn
                result['photo'] = url
                result['source'] = "http://www.librarything.com/search.php?search=%s" % isbn
                return result
            else:
                return None
        except:
            return None

    def check(self):
        return self._run('9780671657130') == {
            'isbn': u'9780671657130',
            'photo': u'http://www.librarything.com/devkey/3f8ba261818a718f42e1c94df68f48b8/large/isbn/9780671657130',
            'source': u'http://www.librarything.com/search.php?search=9780671657130'}

if __name__ == '__main__':
    print LibraryThing().check()
