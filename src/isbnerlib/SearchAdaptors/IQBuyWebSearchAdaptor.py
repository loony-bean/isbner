#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BookInfoWebSearchAdaptor import BookInfoWebSearchAdaptor

class IQBuyWebSearchAdaptor( BookInfoWebSearchAdaptor ):
    def __init__( self ):
        self.name = "iqbuy"

    def getInfo( self, isbn ):
        isbn = self.stripISBN( isbn )

        url = "http://books.iqbuy.ru/categories_offer/%s" % ( isbn, )
        text = self.readStream( url )
        result = { "Title" : "" }

        seriesReg = '<p>%s: (.*?)</p>' % ( "Серия".decode("utf-8").encode("cp1251"), )
        publisherReg = '<p>%s: (.*?)</p>' % ( 'Издательство'.decode("utf-8").encode("cp1251"), )
        
        regs = {
            'Title' : '<h2 class="book-name">(.*?)</h2>',
            'Author' : '<p class="book-author">(.*?)</p>',
            'Series' : seriesReg,
            'Publisher' : publisherReg,
        }

        for k in regs.keys():
            result[k] = self.removeHtmlTags( self.getRegText( regs[k], text ) ).decode("cp1251")

        result["ISBN"] = isbn
        result["Source"] = self.name

        return result

    def getCoverUrl( self, isbn ):
        pass

    def getSourceUrl( self, isbn ):
        pass

def main():
    testList = [
            "9781558601918",
            "9780136006633",
            "0521545668",
            "0882332104"
        ]

    searcher = IQBuyWebSearchAdaptor()

    for el in testList:
        print "%s:" % ( el, ),
        info = searcher.getInfo( el )
        print "[%s]" % ( info["Title"], ),

if __name__ == '__main__':
    main()
