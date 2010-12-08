# -*- coding: utf-8 -*-

from adaptor import Adaptor
from utils import fetch
from BeautifulSoup import BeautifulSoup
import re

rx_data = re.compile('<script(?:.*?)>')
rx_publisher = re.compile('.*?\((\d*)\)')
rx_series = re.compile('<p>�����: <strong>.*?</strong></p>', re.U) # cp1251

class IQBuy(Adaptor):
    def __init__(self):
        self._name = 'IQBuy'
        self._url = 'http://books.iqbuy.ru/'
        self._weight = 10

    def _run(self, isbn):
        url = 'http://books.iqbuy.ru/categories_offer/%s' % (isbn)
        data = rx_data.sub('', fetch(url))
        soup = BeautifulSoup(data)

        try:
            result = dict()
            result['title'] = soup.find('h2', {'class': 'book-name'}).string
            authors = soup.find('p', {'class': 'book-author'})
            # author is optional
            if authors.strong.string:
                result['author'] = authors.strong.string.replace('  ', ' ')
            # series is optional
            series = authors.findNext('p')
            reg = rx_series.search(series.encode("cp1251"))
            if reg:
                result['series'] = series.strong.string
                publisher = series.findNext('p')
            else:
                publisher = series
            # continue with publisher
            result['publisher'] = publisher.strong.string.replace('  ', ' ').strip()
            reg = rx_publisher.search(str(publisher))
            if reg: result['date'] = reg.group(1)
            result['source'] = url
            result['isbn'] = isbn
            return result
        except:
            return None

    def check(self):
        return self._run('9785699306985') == {
            'title': u'12 стульев. Золотой теленок (подарочное издание)',
            'author': u'Илья Ильф, Евгений Петров',
            'series': u'Библиотека великих писателей. Брокгауз - Ефрон',
            'publisher': u'Издательство ЭКСМО',
            'date': u'2008',
            'isbn': u'9785699306985',
            'source': 'http://books.iqbuy.ru/categories_offer/9785699306985'}

if __name__ == '__main__':
    print IQBuy().check()
