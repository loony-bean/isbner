#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi

from datetime import datetime

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db

from isbnerlib import BookInfoModel
from isbnerlib import BookInfoWebSearcher
from MainHandler import MainHandler

class ViewHandler( MainHandler ):
    def __init__( self ):
        self.templateValues = {}
        self.templateValues = { "page" : "../static/index.html" }
        self.templateValues["site"] = { "name" : "view" }

    def get( self ):
        isbn = self.getRequestISBN()
        
        if isbn:
            searcher = BookInfoWebSearcher()
            info = searcher.getInfo( isbn )

            if "Title" in info and info["Title"]:
                keys = info.keys()
                keys.sort()
                self.templateValues["info"] = [ { "key" : k, "value" : info[k] } for k in keys ]

                last = BookInfoModel.all().order("-added").fetch(1)

                if not len( last ) or last[0].ISBN != info["ISBN"]:
                    bookInfo = BookInfoModel( ISBN = info["ISBN"], title = info["Title"], added = datetime.now() )
                    if "Author" in info:
                        bookInfo.author = info["Author"]
                    if "Publisher" in info:
                        bookInfo.publisher = info["Publisher"]
                    if "Series" in info:
                        bookInfo.series = info["Series"]

                    bookInfo.put()

        if cgi.escape( self.request.get('history') ) == "1":
            self.templateValues["history"] = self.getHistory( 10 )

        self.renderTemplate()
