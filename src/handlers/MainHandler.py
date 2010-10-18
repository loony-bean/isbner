#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import cgi

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db

from isbnerlib import BookInfoModel
from isbnerlib import BookInfoWebSearcher

class MainHandler( webapp.RequestHandler ):
    def __init__( self ):
        self.templateValues = {}
        self.templateValues["page"] = "../static/index.html"
        self.templateValues["site"] = { "name" : "booksack" }

    def getRequestISBN( self ):
        isbn = str( cgi.escape( self.request.get('isbn') ) )
        isbn = re.sub( "(-| )", "", isbn )
        return isbn

    def getHistory( self, count ):
        history = BookInfoModel.all()
        history.order( "-added" )
        return history.fetch( count )

    def renderTemplate( self ):
        path = os.path.join(os.path.dirname( __file__ ), self.templateValues["page"] )
        self.response.out.write( template.render( path, self.templateValues ) )

    def get( self ):
        if cgi.escape( self.request.get('history') ) == "1":
            self.templateValues["history"] = self.getHistory( 10 )

        self.renderTemplate()
