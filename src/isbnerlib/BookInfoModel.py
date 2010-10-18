#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class BookInfoModel( db.Model ):
    ISBN = db.StringProperty()
    title = db.StringProperty()
    author = db.StringProperty()
    publisher = db.StringProperty()
    series = db.StringProperty()
    added = db.DateTimeProperty()

def main():
    pass

if __name__ == '__main__':
    main()
