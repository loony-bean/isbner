#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib
from xml.dom import minidom

from BookInfoWebSearchAdaptor import BookInfoWebSearchAdaptor

class ISBNDbWebSearchAdaptor( BookInfoWebSearchAdaptor ):
    def __init__( self ):
        self.name = "isbndb"

    def getInfo( self, isbn ):
        isbn = self.stripISBN( isbn )
        walker = BookXMLWalker()

        info = walker.getInfo( isbn )

        result = { "Title" : "" }

        if info:
            # isbn
            result["ISBN"] = info["isbn"]
            result["ISBN13"] = info["isbn13"]
            # title
            result["Title"] = info["Title"]
            result["Title Long"] = info["TitleLong"]
            # authors
            result["Author"] = info["AuthorsText"]
            # publisher
            result["Publisher"] = info["PublisherText"]["data"]
            # meta
            result["Language"] = info["Details"]["language"]
            result["Summary"] = info["Summary"]
            # phisical
            result["Physical Description"] = info["Details"]["physical_description_text"]
            result["Edition Info"] = info["Details"]["edition_info"]
            # subjects
            result["LCC"] = info["Details"]["lcc_number"]
            result["DCC"] = info["Details"]["dewey_decimal"]
            
        result["Source"] = self.name

        return result

class BookXMLWalker( BookInfoWebSearchAdaptor ):
    def __init__( self ):
        self.website = "http://isbndb.com/api/books.xml"
        self.key = "5CNKTZDN"
        self.keywords = "+".join( [ "details", "texts", "authors", "subjects" ] )
        self.info = {}

    def getInfo( self, isbn ):
        url = "%s?access_key=%s&index1=isbn&value1=%s&results=%s" % ( self.website, self.key, isbn, self.keywords )

        text = self.readStream( url )
        text = re.sub( "\n\n", " ", text )
        text = re.sub( "\n", "", text )
        xmldoc = minidom.parseString( text )

        entries = xmldoc.getElementsByTagName("BookData")

        if entries:
            self.parseDocument( entries[0] )

        return self.info

    def getAttributes( self, node ):
        result = {}
        if len( node.attributes ):
            for i in range( node.attributes.length ):
                key = node.attributes.item(i).name
                value = node.attributes.item(i).nodeValue

                result[key] = value

        return result

    def getElementWithAttributes( self, value, attributes ):
        result = {}
        if attributes:
            result = { u"data" : value }
            for k in attributes.keys():
                result[k] = attributes[k]
        else:
            result = value

        return result

    def parseKey( self, node ):
        key = node.tagName
        value = node.childNodes[0].data

        self.info[key] = self.getElementWithAttributes( value, self.getAttributes( node ) )

    def parseSection( self, node ):
        sectionList = []
        for child in node.childNodes:
            if len( child.childNodes ) == 1 and child.childNodes[0].nodeType == child.TEXT_NODE:
                obj = self.getElementWithAttributes( child.childNodes[0].data, self.getAttributes( child ) )
                sectionList.append( obj )

        self.info[ node.nodeName ] = sectionList

    def parseDocument( self, node ):
        self.info = self.getAttributes( node )

        if len(node.childNodes):
            for child in node.childNodes:
                if len( child.childNodes ) == 0:
                    obj = self.getElementWithAttributes( u"", self.getAttributes( child ) )
                    self.info[child.tagName] = obj

                if len( child.childNodes ) == 1:
                    if child.childNodes[0].nodeType == child.TEXT_NODE:
                        self.parseKey( child )
                    else:
                        self.parseSection( child )

                if len( child.childNodes ) > 1:
                    self.parseSection( child )

        else:
            pass

def main():
    testList = [
            "0316160202",
            "9781558601918",
            "9780136006633",
            "0521545668",
            "0882332104"
        ]

    searcher = ISBNDbWebSearchAdaptor()

    for el in testList:
        print "%s:" % ( el, ),
        info = searcher.getInfo( el )

        print info["Title"]
        print info["Title Long"]

if __name__ == '__main__':
    main()
