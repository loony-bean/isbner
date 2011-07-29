# -*- coding: utf-8 -*-
import re

formats = {
    'schema': {
                'schema': 'itemscope itemtype="http://schema.org/Book"',
                'prop': 'itemprop',
                'fields': {'photo': 'image', 'title': 'name', 'author': 'author',
                    'publisher': 'publisher', 'date': 'publishDate',
                    'isbn': 'isbn', 'url': 'url'},
                'selfrel': False,
                'usetime': True
    },
    'rdfa': {
                'schema': 'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:v="http://rdf.data-vocabulary.org/#" about="http://www.isbner.org/view/?isbn=%s"',
                'prop': 'property',
                'fields': {'photo': 'v:photo', 'title': 'dc:title', 'author': 'dc:creator',
                    'publisher': 'dc:publisher', 'date': 'dc:date',
                    'isbn': 'dc:urn:ISBN', 'url': 'v:url'},
                'selfrel': True,
                'usetime': False
    },
    'microformats': {
                'schema': 'class="Book"',
                'prop': 'class',
                'fields': {'photo': 'photo', 'title': 'title', 'author': 'author',
                    'publisher': 'publisher', 'date': 'date',
                    'isbn': 'isbn', 'url': 'source'},
                'selfrel': False,
                'usetime': False
    }
}
valid = ['schema', 'rdfa', 'microformats', 'raw', 'json']

isodate = lambda date: ''

def markup(format, raw):
    field = lambda k: schema['fields'][k]
    img = lambda value: '<img %s="%s" src="%s" />' % (prop, field('photo'), value)
    span = lambda k, value: '<span %s="%s">%s</span>' % (prop, k, value)
    a = lambda name, url: '<a %s="%s" href="%s">%s</a>' % (prop, field('url'), url, name)
    time = lambda date: '<time %s="%s" datetime="%s">%s</time>' % (prop, field('date'), isodate(date), date)

    if not format in valid:
        format = 'raw'
    data = prepare(raw)
    if format == 'raw':
        for k in data:
            if k == 'photo':
                data[k] = '<img src="%s" />' % data[k]
            elif k == 'sources':
                data[k] = ', '.join('<a href="%s">%s</a>' % (url, name) for name, url in data[k])
    elif format == 'json':
        pass
    else:
        schema = formats[format]
        prop = schema['prop']
        head = schema['schema']
        data['schema'] = schema['selfrel'] and head % data['isbn'] or head
        for k in data:
            v = data[k]
            if k == 'photo': data[k] = img(v)
            elif k == 'date': data[k] = schema['usetime'] and time(v) or span(field(k), v)
            elif k == 'sources': data[k] = ', '.join([a(name, url) for name, url in v])
            else:
                if k in schema['fields']:
                    data[k] = span(field(k), v)
    return data

def ordered_pairs(data):
    keys = ['photo', 'title', 'author', 'publisher', 'date', 'isbn', 'sources']
    keys = keys + filter(lambda k: k not in keys, data.keys())
    keys = filter(data.has_key, keys)
    return [(k, data[k]) for k in keys]

def prepare(raw):
    result = dict()
    for k in raw['fields']:
        result[k] = raw['fields'][k][0]
    if 'sources' in raw and raw['sources']:
        result['sources'] = [(k, raw['sources'][k]) for k in raw['sources']]
    return result

def truncate_urls(data):
    urls = re.findall(u'"(http:.*?)"', data)
    maxlen = 35
    tail = '…'
    for url in urls:
        if len(url) > maxlen - len(tail):
            data = data.replace(url, '%s%s' % (url[:maxlen], tail))
    return data

