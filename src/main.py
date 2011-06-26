# -*- coding: utf-8 -*-

import logging, sys, os
#from google.appengine.dist import use_library; use_library('django', '1.2')
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
        format = self.request.get('format')
        if not isbn:
            self.response.set_status(404)
        else:
            data = memcache.get(isbn, namespace='isbn')
            if not data:
                self.response.set_status(204)
                data = isbner.stub
                for worker in isbner.names:
                    taskqueue.add(url='/worker/%s' % worker, params={'isbn': isbn})
            else:
                self.response.set_status(200)
            data = isbner.formats.markup(format, data)
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(simplejson.dumps(data))

class ViewHandler(webapp.RequestHandler):
    def get(self):
        isbn = self.request.get('isbn')
        format = self.request.get('format') or 'raw'
        template_values = {'book': {'isbn': isbn, 'format': format}}
        try:
            # Practice what you preach
            host_url = self.request.host_url.replace('8080', '8081')
            data = simplejson.loads(isbner.utils.fetch('%s/get/?isbn=%s&format=%s' % (host_url, isbn, format)))
        except:
            pass
        else:
            formats = list()
            for name in isbner.formats.valid:
                if name != format:
                    formats.append('<a href = "/view/?isbn=%(isbn)s&format=%(format)s">%(format)s</a>' % {'format': name, 'isbn': isbn})
                else:
                    formats.append(name)
            template_values['formats'] = ', '.join(formats)

            if format == 'json':
                template_values['json'] = data
            else:
                for field in ('photo', 'schema'):
                    if field in data: template_values[field] = data.pop(field)
                data['format'] = format
                template_values['info'] = isbner.formats.ordered_pairs(data)
                html = os.path.join(os.path.dirname(__file__), 'static', 'fields.html')
                src = template.render(html, template_values)
                template_values['html'] = isbner.formats.truncate_urls(src)

        path = 'fields.html' if self.request.get('fields') else 'view.html'
        path = os.path.join(os.path.dirname(__file__), 'static', path)
        result = template.render(path, template_values)
        self.response.out.write(result)

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
    urls = ['/', '/terms/', '/api/', '/opensearch-description.xml']
    filenames = ['index.html', 'terms.html', 'api.html', 'opensearch-description.xml']
    for (url, filename) in zip(urls, filenames):
        class StaticHandler(webapp.RequestHandler):
            def get(self):
                demo = dict()
                if self.name == 'index.html':
                    json = open('static/demo.js').read()
                    data = simplejson.loads(json)
                    for format in isbner.formats.valid:
                        marked = isbner.formats.markup(format, data)
                        html = os.path.join(os.path.dirname(__file__), 'static', 'demo.html')
                        src = template.render(html, {'book': marked})
                        marked['html'] = isbner.formats.truncate_urls(src)
                        demo[format] = template.render(html, {'book': marked})
                    demo['json'] = isbner.formats.truncate_urls(json)
                path = os.path.join(os.path.dirname(__file__), 'static', self.name)
                self.response.out.write(template.render(path, {'book': demo}))
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
