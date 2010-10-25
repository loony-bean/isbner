# -*- coding: utf-8 -*-

from amazon import Amazon
from livelib import LiveLib
from openlibrary import OpenLibrary
from labirint import Labirint

all = [LiveLib, Amazon, OpenLibrary, Labirint]
names = map(lambda a: a().name, all)
