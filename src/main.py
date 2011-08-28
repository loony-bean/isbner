# -*- coding: utf-8 -*-

import logging, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
from urlparse import urljoin

from flask import Flask, Markup, jsonify, request, redirect, url_for, \
     abort, render_template
#from flask import json
import simplejson as json

from google.appengine.api import taskqueue
from google.appengine.ext.webapp import util
from google.appengine.api import memcache

import isbner

# configuration
DEBUG = False

# create and application
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_pyfile('isbner/credentials.py')

# Custom template filters
@app.template_filter()
def linebreakbr(s):
    return s.replace('\n', Markup('<br>'))

@app.template_filter()
def truncate_urls(data):
    return isbner.formats.truncate_urls(data)

@app.route('/get/')
def get():
    isbn = isbner.utils.sanitize(request.args.get('isbn'))
    format = request.args.get('format')
    status_code = 200

    if not isbn:
        abort(404)
    else:
        data = memcache.get(isbn, namespace='isbn')
        if not data:
            status_code = 204
            data = isbner.stub
            for worker in isbner.names:
                taskqueue.add(url='/worker/%s' % worker, params={'isbn': isbn})

        data = isbner.formats.markup(format, data)
        response = jsonify(data)
        response.status_code = status_code
        return response

@app.route('/view/')
def view():
    isbn = isbner.utils.sanitize(request.args.get('isbn')) or ''
    return render_template('view.html', **{'book': {'isbn': isbn}})

@app.route('/view/fields/')
def fields():
    isbn = request.args.get('isbn')
    format = request.args.get('format') or 'raw'
    template_values = {'book': {'isbn': isbn, 'format': format}}

    try:
        # Practice what you preach
        base_url = request.url_root.replace('8080', '8081')
        get_url = url_for('get', isbn=isbn, format=format)
        fetch = isbner.utils.fetch(urljoin(base_url, get_url))
        data = json.loads(fetch)
    except:
        abort(404)
    else:
        formats = list()
        for name in isbner.formats.valid:
            if name != format:
                format_url = urljoin(base_url,
                                     url_for('get', isbn=isbn, format=name))
                formats.append('<a target=_blank href = "%s">%s</a>' % \
                               (format_url, name))
        template_values['formats'] = ', '.join(formats)

        if format == 'json':
            template_values['json'] = data
        else:
            for field in ('photo', 'schema'):
                if field in data: template_values[field] = data.pop(field)
            template_values['info'] = isbner.formats.ordered_pairs(data)

    return render_template('fields.html', **template_values)

@app.route('/providers/')
def providers():
    return render_template('providers.html', info=memcache.get('status'))

@app.route('/status/')
def status():
    for worker in isbner.names:
        taskqueue.add(url='/worker/%s' % worker, params={'check': '1'})
    return app.make_response('')

def workers_factory():
    for (name, adaptor_class) in zip(isbner.names, isbner.classes):
        def adaptor_worker(adaptor = adaptor_class()):
            def check():
                data = memcache.get('status') or dict()
                data[adaptor.name] = adaptor.check()
                memcache.set('status', data, time=86400)

            def run(isbn):
                isbn = isbner.utils.sanitize(isbn)
                data = adaptor.dump(isbn)
                cached = memcache.get(isbn, namespace='isbn')
                if cached is not None:
                    data = isbner.utils.merge(cached, data)
                memcache.set(isbn, data, time=86400, namespace='isbn')

            if request.values.get('check'):
                check()
            else:
                run(request.values.get('isbn'))
            return app.make_response('')

        yield((name, adaptor_worker))

def statics_factory():
    urls = ['/', '/terms/', '/api/', '/opensearch-description.xml']
    filenames = ['index.html', 'terms.html', 'api.html', 'opensearch-description.xml']
    for (url, filename) in zip(urls, filenames):
        def static_page(name = filename):
            demo = dict()
            if name == 'index.html':
                json_src = open('templates/demo.js').read()
                data = json.loads(json_src)
                for format in isbner.formats.valid:
                    demo[format] = isbner.formats.markup(format, data)

                demo['json'] = isbner.formats.truncate_urls(json_src)
            return render_template(name, book=demo)

        yield((url, static_page))

def main():
    for (url, static) in statics_factory():
        app.add_url_rule(url, url, static)
    for (name, worker) in workers_factory():
        app.add_url_rule('/worker/%s' % name, name, worker, methods=['POST'])

    util.run_wsgi_app(app)

if __name__ == '__main__':
    main()
