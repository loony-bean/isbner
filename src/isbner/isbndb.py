# -*- coding: utf-8 -*-

from adaptor import Adaptor
from utils import fetch
from credentials import ISBNDB_ACCESS_KEY
from BeautifulSoup import BeautifulSoup
import re

rx_publisher = re.compile('(.*?)(?::|;)(.*), (c)?(\d*)')
rx_edition = re.compile('.*?([\d-]+)')

class ISBNDb(Adaptor):
    def __init__(self):
        self._name = 'ISBNDb'
        self._url = 'http://isbndb.com/'
        self._weight = 40

    def _run(self, isbn):
        keywords = '+'.join(['details', 'texts', 'authors', 'subjects'])
        url = 'http://isbndb.com/api/books.xml?access_key=%s&index1=isbn&value1=%s&results=%s' % (ISBNDB_ACCESS_KEY, isbn, keywords)
        soup = BeautifulSoup(fetch(url))

        try:
            result = dict()
            result['title'] = soup.find('titlelong').string or soup.find('title').string
            result['author'] = soup.find('authorstext').string
            bookdata = soup.find('bookdata').attrs
            result['isbn'] = bookdata[2][1]
            result['source'] = 'http://isbndb.com/d/book/%s.html' % bookdata[0][1]
            # publisher info
            pubs = soup.find('publishertext').string
            reg = rx_publisher.search(pubs)
            if reg:
                if len(reg.groups()) == 1:
                    result['publisher'] = reg.group(1)
                elif len(reg.groups()) == 4:
                    result['publisher'] = reg.group(2).strip()
                    result['date'] = reg.group(4).strip()
            # date also can be found in details->edition_info->date
            if not 'date' in result:
                details = soup.find('details').attrs
                for e in details:
                    if u'edition_info' == e[0]:
                        reg = rx_edition.search(e[1])
                        if reg: result['date'] = reg.group(1)
            return result
        except:
            return None

    def check(self):
        return self._run('0201558025') == {
            'title': u'Concrete mathematics: a foundation for computer science',
            'author': u'Ronald L. Graham, Donald E. Knuth, Oren Patashnik',
            'isbn': u'9780201558029',
            'publisher': u'Addison-Wesley',
            'date': u'1994',
            'source': u'http://isbndb.com/d/book/concrete_mathematics_a01.html'}

if __name__ == '__main__':
    print ISBNDb().check()
