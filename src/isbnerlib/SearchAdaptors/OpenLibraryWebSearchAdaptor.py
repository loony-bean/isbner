#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BookInfoWebSearchAdaptor import BookInfoWebSearchAdaptor

class OpenLibraryWebSearchAdaptor( BookInfoWebSearchAdaptor ):
    def __init__( self ):
        self.name = "openlibrary"
        #http://openlibrary.org/developers/api

def main():
    pass

if __name__ == '__main__':
    main()
