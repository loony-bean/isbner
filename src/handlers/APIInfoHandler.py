#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import simplejson
from isbnerlib import BookInfoWebSearcher
from MainHandler import MainHandler

class APIInfoHandler( MainHandler ):
    def __init__( self ):
        self.templateValues = {}
        self.templateValues["page"] = "../static/api/info.html"
        self.templateValues["site"] = { "name" : "api" }

    def get( self ):
        isbn = self.getRequestISBN()

        if isbn:
            searcher = BookInfoWebSearcher()
            info = searcher.getInfo( isbn )
            if info["Title"]:
                self.templateValues["content"] = simplejson.dumps( info )

        self.renderTemplate()
