#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import urllib

class BookInfoWebSearchAdaptor():
    def __init__( self ):
        pass

    def stripISBN( self, isbn ):
        # TODO
        return re.sub( "(-| )", "", isbn )

    def getInfo( self, isbn ):
        pass

    def getCoverUrl( self, isbn ):
        pass

    def getSourceUrl( self, isbn ):
        pass

    def readStream( self, url ):
        text = ""

        try:
            stream = urllib.urlopen( url )
            if stream:
                text = stream.read()
        finally:
            stream.close()

        """
        #streamRepeatOpening = True
        #while streamRepeatOpening:
        try:
            stream = urllib.urlopen( url )
            if stream:
                text = stream.read()
                if text:
                    streamRepeatOpening = False
                    stream.close()
        except:
            pass
        """

        return text

    def removeHtmlTags( self, text ):
        return re.sub( "<.*?>", "", text )

    def getRegText( self, reg, text ):
        r = re.search( reg, text, re.S + re.U + re.I )

        if r:
            value = r.group(1)
        else:
            value = ""

        return value


def main():
    pass

if __name__ == '__main__':
    main()
