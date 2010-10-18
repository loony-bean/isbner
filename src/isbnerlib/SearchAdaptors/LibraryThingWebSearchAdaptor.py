#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BookInfoWebSearchAdaptor import BookInfoWebSearchAdaptor

class LibraryThingWebSearchAdaptor( BookInfoWebSearchAdaptor ):
    def __init__( self ):
        self.name = "librarything"
        #http://www.librarything.com/services/

def main():
    pass

if __name__ == '__main__':
    main()
