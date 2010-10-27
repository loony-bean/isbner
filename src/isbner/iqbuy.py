# -*- coding: utf-8 -*-

from adaptor import Adaptor
from utils import fetch
import re

class IQBuy(Adaptor):
    def __init__(self):
        self._name = 'IQBuy'
        self._weight = 10

    def _run(self, isbn):
        from BeautifulSoup import BeautifulSoup

        url = 'http://books.iqbuy.ru/categories_offer/%s' % (isbn)
        data = re.sub('<script(?:.*?)>', '', fetch(url))
        soup = BeautifulSoup(data)

        try:
            result = dict()
            result['title'] = soup.find('h2', {'class': 'book-name'}).string
            authors = soup.find('p', {'class': 'book-author'})
            result['author'] = authors.strong.string.replace('  ', ' ')
            series = authors.findNext('p')
            result['series'] = series.strong.string
            print result['series']
            publisher = series.findNext('p')
            result['publisher'] = publisher.strong.string.replace('  ', ' ').strip()
            reg = re.search('.*?\((\d*)\)', str(publisher))
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

def main():
    print IQBuy().check()

if __name__ == '__main__':
    main()
