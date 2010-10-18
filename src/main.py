#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext.webapp import util
from google.appengine.ext import webapp

from handlers import *

def main():
    application = webapp.WSGIApplication( [( '/', MainHandler ),
                                           ( '/view/?', ViewHandler ),
                                           ( '/api/info/?', APIInfoHandler ),
                                          ],
                                          debug=True )
    util.run_wsgi_app( application )

if __name__ == '__main__':
    main()
