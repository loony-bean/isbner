# -*- coding: utf-8 -*-

from adaptor import Adaptor
from BeautifulSoup import BeautifulSoup
from utils import fetch

class LiveLib(Adaptor):
    def __init__(self):
        self._name = 'LiveLib'
        self._url = 'http://www.livelib.ru/'
        self._weight = 10

    def _run(self, isbn):
        url = 'http://www.livelib.ru/find/%s' % isbn
        soup = BeautifulSoup(fetch(url))

        try:
            result = dict()
            result['title'] = soup.find('div', {'class': 'title'}).a.string
            result['author'] = soup.find('a', {'class': 'author unnoticeable'}).string
            span_info = soup.find('span', {'class': 'info'})
            result['publisher'] = span_info.string.replace('&laquo;', '').replace('&raquo;', '')
            span_info = span_info.nextSibling
            span_info = span_info.nextSibling
            result['date'] = span_info.string.replace(u' г.', '')
            span_info = span_info.nextSibling
            span_info = span_info.nextSibling
            result['isbn'] = isbn #span_info.string.replace(u'ISBN: ', '').replace('-', '')
            result['source'] = url
            result['photo'] = soup.find('div', {'class': 'thumbnail'}).a.img['src'].replace('/s/','/l/') # small size -> large
            return result
        except:
            return None

    def check(self):
        return self._run('9785379003067') == {
            'title': u'Введение в математическую философию',
            'author': u'Бертран Рассел',
            'publisher': u'Сибирское университетское издательство',
            'date': u'2007',
            'isbn': u'9785379003067',
            'photo': u'http://j.livelib.ru/boocover/1000444518/l/e193/Bertran_Rassel__Vvedenie_v_matematicheskuyu_filosofiyu.gif',
            'source': u'http://www.livelib.ru/find/9785379003067'}

if __name__ == '__main__':
    print LiveLib().check()
