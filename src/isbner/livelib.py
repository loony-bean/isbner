# -*- coding: utf-8 -*-

from adaptor import Adaptor
from utils import fetch

class LiveLib(Adaptor):
    def __init__(self):
        self._name = "LiveLib"
        self._weight = 10

    def _run(self, isbn):
        from BeautifulSoup import BeautifulSoup

        url = "http://www.livelib.ru/find/%s" % (isbn)
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
            result['isbn'] = span_info.string.replace(u'ISBN: ', '').replace('-', '')
            result['source'] = url
            return result
        except:
            return None

    def check(self):
        return self._run('9785379003067') == {
            'title': u'Введение в математическую философию',
            'author': u'Бертран Рассел',
            'publisher': u'Сибирское университетское издательство',
            'date': u'2007',
            'isbn': u'9785379003067, 5379003060',
            'source': u'http://www.livelib.ru/find/9785379003067'}
