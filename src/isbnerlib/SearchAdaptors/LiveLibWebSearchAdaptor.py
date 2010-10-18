#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BookInfoWebSearchAdaptor import BookInfoWebSearchAdaptor

class LiveLibWebSearchAdaptor( BookInfoWebSearchAdaptor ):
    def __init__( self ):
        self.name = "livelib"

    def getInfo( self, isbn ):
        isbn = self.stripISBN( isbn )

        url = "http://www.livelib.ru/find/%s" % ( isbn, )
        text = self.readStream( url )
        result = { "Title" : "" }

        result["Title"] = self.removeHtmlTags( self.getRegText( '<div class="title".*?>(.*?)</div>', text ) ).decode("utf-8")
        result["Author"] = self.removeHtmlTags( self.getRegText( '<a class="author unnoticeable".*?>(.*?)</a>', text ) ).decode("utf-8")
        result["ISBN"] = isbn
        result["Source"] = self.name

        return result

def main():
    pass

if __name__ == '__main__':
    main()
