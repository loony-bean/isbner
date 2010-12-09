# -*- coding: utf-8 -*-

import logging
import os
from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from django.utils import simplejson

import isbner

class GetHandler(webapp.RequestHandler):
    def get(self):
        isbn = isbner.utils.sanitize(self.request.get('isbn'))
        if not isbner.utils.validate(isbn):
            data = isbner.stub
            self.response.set_status(200)
        else:
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
    # TODO: Looks horrible enough to be refactored
    def get(self):
        isbn = isbner.utils.sanitize(self.request.get('isbn'))
        template_values = {'book': {'isbn': isbn}}
        if self.request.get('fields'):
            path = os.path.join(os.path.dirname(__file__), 'static', 'fields.html')
        else:
            path = os.path.join(os.path.dirname(__file__), 'static', 'view.html')
        if not isbner.utils.validate(isbn):
            template_values['message'] = "ISBN is not valid."
            return self.response.out.write(template.render(path, template_values))
        else:
            template_values['message'] = "Waiting for data..."
        try:
            # Practice what you preach
            host_url = self.request.host_url.replace('8080', '8081')
            data = simplejson.loads(isbner.utils.fetch('%s/get/?isbn=%s' % (host_url, isbn)))
        except:
            pass
        else:
            # cover photo
            if 'photo' in data['fields']:
                template_values['photo'] = data['fields']['photo'][0]
                del data['fields']['photo']
            # data fields
            fields = ['title', 'author', 'publisher', 'date', 'isbn']
            keys = fields + list(set(data['fields'].keys()) - set(fields))
            keys = [k for k in keys if k in data['fields'].keys()]
            # sources
            data['fields']['source'] = [', '.join(
                ['<a href="%s">%s</a>' % (data['sources'][k], k) for k in data['sources'].keys()])]
            if data['fields']['source'][0]:
                keys.append('source')
            template_values['info'] = [{'key': k, 'value': data['fields'][k][0]} for k in keys]
        self.response.out.write(template.render(path, template_values))

class ProvidersHandler(webapp.RequestHandler):
    def get(self):
        template_values = {'info': memcache.get('status')}
        path = os.path.join(os.path.dirname(__file__), 'static', 'providers.html')
        self.response.out.write(template.render(path, template_values))

class StatusHandler(webapp.RequestHandler):
    def get(self):
        for worker in isbner.names:
            taskqueue.add(url='/worker/%s' % worker, params={'check': '1'})
        self.response.set_status(200)

def workers_factory():
    for (name, adaptor_class) in zip(isbner.names, isbner.classes):
        class AdaptorWorker(webapp.RequestHandler):
            def check(self):
                data = memcache.get('status') or dict()
                data[self.adaptor.name] = self.adaptor.check()
                memcache.set('status', data, time=86400)

            def run(self, isbn):
                isbn = isbner.utils.sanitize(isbn)
                data = self.adaptor.dump(isbn)                
                cached = memcache.get(isbn, namespace='isbn')
                if cached is not None:
                    data = isbner.utils.merge(cached, data)
                memcache.set(isbn, data, time=86400, namespace='isbn')

            def post(self):
                if self.request.get('check'):
                    self.check()
                else:
                    self.run(self.request.get('isbn'))
                self.response.set_status(200)

            adaptor = adaptor_class()
        yield((name, AdaptorWorker))

def statics_factory():
    urls = ['/', '/terms/', '/api/']
    filenames = ['index.html', 'terms.html', 'api.html']
    for (url, filename) in zip(urls, filenames):
        class StaticHandler(webapp.RequestHandler):
            def get(self):
                path = os.path.join(os.path.dirname(__file__), 'static', self.name)
                self.response.out.write(template.render(path, {}))
            name = filename
        yield((url, StaticHandler))

def main():
    urls = [('/get/?', GetHandler),
            ('/view/?', ViewHandler),
            ('/status/', StatusHandler),
            ('/providers/', ProvidersHandler)]
    for (url, worker) in statics_factory():
        urls.append((url, worker))
    for (name, worker) in workers_factory():
        urls.append(('/worker/%s' % name, worker))

    webapp.util.run_wsgi_app(webapp.WSGIApplication(urls, debug=True))

if __name__ == '__main__':
    main()
