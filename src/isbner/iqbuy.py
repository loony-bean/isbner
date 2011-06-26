# -*- coding: utf-8 -*-

from adaptor import Adaptor
from utils import fetch
from BeautifulSoup import BeautifulSoup
import re

rx_data = re.compile(u'<script(?:.*?)>', re.U)
rx_publisher = re.compile(u'.*?\((\d*)\)', re.U)
rx_series = re.compile(u'<p>Серия: <strong>.*?</strong></p>', re.U)

class IQBuy(Adaptor):
    def __init__(self):
        self._name = 'IQBuy'
        self._url = 'http://books.iqbuy.ru/'
        self._weight = 10

    def _run(self, isbn):
        url = 'http://books.iqbuy.ru/categories_offer/%s' % (isbn)
        data = rx_data.sub('', fetch(url).decode('cp1251'))
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
            reg = rx_series.search(unicode(series))
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
            result['photo'] = soup.find('td', {'class': 'book-image'}).p.img['src']
            return result
        except:
            return None

    def check(self):
        return self._run('9785699306985') == {
            'title': u'Двенадцать стульев. Золотой теленок',
            'author': u'Илья Ильф, Евгений Петров',
            'series': u'Библиотека великих писателей. Брокгауз - Ефрон',
            'publisher': u'Издательство ЭКСМО',
            'date': u'2008',
            'isbn': u'9785699306985',
            'photo': u'http://books.iqbuy.ru/img/books/9785/69/93/06/98/9785699306985-b.jpg',
            'source': 'http://books.iqbuy.ru/categories_offer/9785699306985'}

if __name__ == '__main__':
    print IQBuy().check()
