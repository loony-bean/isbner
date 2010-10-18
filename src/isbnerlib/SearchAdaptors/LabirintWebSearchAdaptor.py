#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from BookInfoWebSearchAdaptor import BookInfoWebSearchAdaptor

class LabirintWebSearchAdaptor( BookInfoWebSearchAdaptor ):
    def __init__( self ):
        self.name = "labirint.ru"

    def getInfo( self, isbn ):
        isbn = self.stripISBN( isbn )

        url = "http://www.labirint.ru/search/?txt=%s" % ( isbn, )
        text = self.readStream( url )
        result = { "Title" : "" }

        result["Title"] = self.getRegText( '<div id="product-title">.*<h1>.*?: (.*)</h1>', text ).decode("cp1251")

        details = self.getRegText( '<div id="product-specs">(.*)<!--product-specs-->', text )
        if details:
            result["ISBN"] = self.getRegText( '<div class="isbn smallbr">ISBN: (.*?)</div>', details )
            result["Author"] = self.getRegText( '<a href="/authors/.*?">(.*?)</a>', details ).decode("cp1251")
            result["Publisher"] = self.getRegText( '<a href="/pubhouse/.*?">(.*?)</a>', details ).decode("cp1251")
            result["Series"] = self.getRegText( '<a href="/series/.*?">(.*?)</a>', details ).decode("cp1251")
            result["Year"] = self.getRegText( '<a href="/pubhouse/.*?">.*?</a>, (\d*).*?</div>', details )
            result["Pages Count"] = self.getRegText( '<div class="pages2">.*?: (\d*).*</div>', details )
            result["Paper"] = self.getRegText( '<div class="pages2">.*?\((.*?)\)</div>', details ).decode("cp1251")
            result["Weight"] = self.getRegText( '<div class="weight">.*?: (\d*).*</div>', details )

            result["Dimensions"] = self.getRegText( '<div class="dimensions smallbr">.*?: (.*?) .*?</div>', details )

            result["Source"] = self.name

        return result

def main():
    testList = [
            "9785379003067",
            "9785910450855",
            "9781558601918",
            "9785373035408",
        ]

    testList2 = [
            "9785379003067",
        ]

    searcher = LabirintWebSearchAdaptor()

    for el in testList:
        print "%s:" % ( el, ),
        info = searcher.getInfo( el )

        print (",").join( info.keys() )
        if "ISBN" in info:
            for k in info.keys():
                print "%s : %s" % ( k, info[k].decode("cp1251") )
        else:
            print "Not found"

if __name__ == '__main__':
    main()
