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

class GetHandler(webapp.RequestHandler):
    def get(self):
        isbn = isbner.utils.sanitize(self.request.get('isbn'))
        data = memcache.get(isbn, namespace='isbn')
        if data is not None:
            self.response.set_status(200)
        else:
            data = isbner.stub
            for worker in isbner.names:
                taskqueue.add(url='/worker/%s' % worker, params={'isbn': isbn})
            self.response.set_status(204)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps(data))

class ViewHandler(webapp.RequestHandler):
    def get(self):
        isbn = isbner.utils.sanitize(self.request.get('isbn'))
        template_values = {'site': {'name': SITE_NAME},
                           'book': {'isbn': isbn}}
        if self.request.get('fields'):
            path = os.path.join(os.path.dirname(__file__), 'static/fields.html')
        else:
            path = os.path.join(os.path.dirname(__file__), 'static/view.html')
        try:
            host_url = self.request.host_url
            if host_url.find('localhost') > 0:
                host_url = 'http://localhost:8081'
            # Practice what you preach
            data = simplejson.loads(isbner.utils.fetch('%s/get/?isbn=%s' % (host_url, isbn)))           
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
    for (name, adaptor_class) in zip(isbner.names, isbner.classes):
        class AdaptorWorker(webapp.RequestHandler):
            def post(self):
                isbn = isbner.utils.sanitize(self.request.get('isbn'))
                data = self.adaptor.dump(isbn)
                if data is not None:
                    cached = memcache.get(isbn, namespace='isbn')
                    if cached is not None:
                        data = isbner.utils.merge(cached, data)
                    memcache.set(isbn, data, time=86400, namespace='isbn')
                    self.response.set_status(200)
            adaptor = adaptor_class()
        yield((name, AdaptorWorker))

def statics_factory():
    urls = ['/', '/terms/', '/api/', '/status/']
    filenames = ['index.html', 'terms.html', 'api.html', 'status.html']
    for (url, filename) in zip(urls, filenames):
        class StaticHandler(webapp.RequestHandler):
            def get(self):
                path = os.path.join(os.path.dirname(__file__), 'static', self.name)
                self.response.out.write(template.render(path, {}))
            name = filename
        yield((url, StaticHandler))

def main():
    urls = [('/get/?', GetHandler),
            ('/view/?', ViewHandler)]
    for (url, worker) in statics_factory():
        urls.append((url, worker))
    for (name, worker) in workers_factory():
        urls.append(('/worker/%s' % name, worker))

    webapp.util.run_wsgi_app(webapp.WSGIApplication(urls, debug=True))

if __name__ == '__main__':
    main()
