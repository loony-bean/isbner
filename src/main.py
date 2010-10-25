# -*- coding: utf-8 -*-

import logging
import os
from google.appengine.api.labs import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from django.utils import simplejson

import isbner

class MainHandler(webapp.RequestHandler):
    def get(self):
        template_values = {'site': {'name': 'booksack'}}
        path = os.path.join(os.path.dirname(__file__), 'static/index.html')
        self.response.out.write(template.render(path, template_values))

class StatusHandler(webapp.RequestHandler):
    def get(self):
        template_values = {'site': {'name': 'booksack'}}
        path = os.path.join(os.path.dirname(__file__), 'static/status.html')
        self.response.out.write(template.render(path, template_values))

class GetHandler(webapp.RequestHandler):
    def get(self):
        isbn = isbner.utils.sanitize(self.request.get('isbn'))
        data = memcache.get(isbn, namespace='isbn')
        if data is not None:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.set_status(200)
            self.response.out.write(simplejson.dumps(data))
        else:
            self.error(404)

class ViewHandler(webapp.RequestHandler):
    def get(self):
        isbn = isbner.utils.sanitize(self.request.get('isbn'))
        for worker in isbner.names:
            taskqueue.add(url='/worker/%s' % worker, params={'isbn': isbn})

        template_values = {'site': {'name': 'booksack'},
                           'book': {'isbn': isbn}}
        path = os.path.join(os.path.dirname(__file__), 'static/index.html')
        try:
            data = simplejson.loads(isbner.utils.fetch('%s/get/?isbn=%s' % (self.request.host_url, isbn)))
        except:
            pass
        else:
            fields = ['title', 'author', 'publisher', 'date', 'isbn']
            keys = fields + list(set(data['fields'].keys()) - set(fields))
            keys = [k for k in keys if k in data['fields'].keys()]
            data['fields']['source'] = [', '.join(
                ['<a href="%s">%s</a>' % (data['sources'][k], k) for k in data['sources'].keys()])]
            keys.append('source')
            template_values['info'] = [{'key': k, 'value': data['fields'][k][0]} for k in keys]
        self.response.out.write(template.render(path, template_values))

def workers_factory():
    for (name, adaptor_class) in zip(isbner.names, isbner.all):
        class AdaptorWorker(webapp.RequestHandler):
            def post(self):
                isbn = isbner.utils.sanitize(self.request.get('isbn'))
                data = self.adaptor.dump(isbn)
                if data is not None:
                    cached = memcache.get(isbn, namespace='isbn')
                    if cached is not None:
                        data = isbner.utils.merge(cached, data)
                    memcache.set(isbn, data, namespace='isbn')
                    self.response.set_status(200)
            adaptor = adaptor_class()

        yield((name, AdaptorWorker))

def main():
    urls = [('/', MainHandler),
            ('/get/?', GetHandler),
            ('/view/?', ViewHandler),
            ('/status/', StatusHandler)]

    for (name, worker) in workers_factory():
        urls.append(('/worker/%s' % name, worker))

    webapp.util.run_wsgi_app(webapp.WSGIApplication(urls, debug=True))

if __name__ == '__main__':
    main()
