# -*- coding: utf-8 -*-

from adaptor import Adaptor
from utils import fetch
import re

class Labirint(Adaptor):
    def __init__(self):
        self._name = 'Labirint'
        self._weight = 10

    def run(self, isbn):
        from BeautifulSoup import BeautifulSoup

        url = 'http://www.labirint.ru/search/?txt=%s' % (isbn)

        try:
            reg = re.search('<!-- content -->(.*)<!--product-info-->', fetch(url).decode('cp1251'), re.S)
            soup = BeautifulSoup(reg.group(0))

            result = dict()
            result['title'] = soup.find('span', {'class': 'fn'}).next.next.attrs[1][1]
            result['photo'] = soup.find('span', {'class': 'photo'}).next.next.attrs[1][1]
            result['series'] = soup.find('span', {'class': 'category'}).next.next.attrs[1][1]
            result['publisher'] = soup.find('span', {'class': 'brand'}).next.next.attrs[1][1]
            div = soup.find('div', {'class': 'isbn smallbr'})
            result['isbn'] = div.next.replace('ISBN: ', '')
            div = div.findNext('div')
            result['author'] = div.next.next.string
            div = div.findNext('div')
            reg = re.search('.*?(\d+)', div.next.next.next.next)
            if reg: result['date'] = reg.group(1)
            result['source'] = url
            return result
        except Exception, e:
            print e
            return None

    def check(self):
        return self.run('9785379003067') == {
            'title': u'Введение в математическую философию',
            'photo': u'http://img.labirint.ru/images/books4/150957/big.jpg',
            'series': u'Пути философии',
            'publisher': u'Сибирское университетское издательство',
            'isbn': u'978-5-379-00306-7',
            'author': u'Рассел Бертран',
            'date': u'2007',
            'source': 'http://www.labirint.ru/search/?txt=9785379003067'}

def main():
    print Labirint().check()

if __name__ == '__main__':
    main()
