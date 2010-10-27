# -*- coding: utf-8 -*-

from adaptor import Adaptor
from utils import fetch

class Labirint(Adaptor):
    def __init__(self):
        self._name = "Labirint"
        self._weight = 10

    def _run(self, isbn):
        from BeautifulSoup import BeautifulSoup

        url = "http://www.labirint.ru/search/?txt=%s" % isbn
        soup = BeautifulSoup(fetch(url))

        result = dict()
        result['source'] = url
        return None

    def check(self):
        return self._run('9785379003067') == {
            'title': u'Введение в математическую философию',
            'author': u'Бертран Рассел',
            'date': u'2007',
            'isbn': u'9785379003067',
            'source': 'http://www.labirint.ru/search/?txt=9785379003067'}



