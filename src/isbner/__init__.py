# -*- coding: utf-8 -*-

from amazon import Amazon
from livelib import LiveLib
from openlibrary import OpenLibrary
from labirint import Labirint

STUB = {'fields': {}, 'sources': {}}

classes = [LiveLib, Amazon, OpenLibrary, Labirint]
names = map(lambda a: a().name, classes)
