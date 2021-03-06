# -*- coding: utf-8 -*-

from adaptor import Adaptor
from credentials import AMAZON_LICENSE_KEY, AMAZON_SECRET_ACCESS_KEY
import ecs

class Amazon(Adaptor):
    def __init__(self):
        self._name = 'Amazon'
        self._url = 'http://www.amazon.com/'
        self._weight = 55

    def _run(self, isbn):
        ecs.setLicenseKey(AMAZON_LICENSE_KEY)
        ecs.setSecretAccessKey(AMAZON_SECRET_ACCESS_KEY)

        try:
            result = dict()
            item = ecs.ItemSearch(isbn, SearchIndex='Books')
            result['title'] = item[0].Title
            result['author'] = item[0].Author                
            result['publisher'] = item[0].Manufacturer
            result['isbn'] = isbn
            result['source'] = item[0].DetailPageURL
            for k in result.keys():
                if result[k].__class__.__name__ == 'list':
                    result[k] = ', '.join(result[k])
            return result
        except:
            return None

    def check(self):
        return self._run('9780671201586') == {
            'title': u'A History of Western Philosophy',
            'author': u'Bertrand Russell',
            'isbn': u'9780671201586',
            'publisher': u'Simon & Schuster/Touchstone',
            'source': u'http://www.amazon.com/History-Western-Philosophy-Bertrand-Russell/dp/0671201581%3FSubscriptionId%3D08KV218JP5M36AMTFY02%26tag%3Dws%26linkCode%3Dxm2%26camp%3D2025%26creative%3D165953%26creativeASIN%3D0671201581'}

if __name__ == '__main__':
    print Amazon().check()
