# -*- coding: utf-8 -*-

from adaptor import Adaptor
from amazon import Amazon
from livelib import LiveLib
from openlibrary import OpenLibrary
from labirint import Labirint
from iqbuy import IQBuy
from isbndb import ISBNDb
from librarything import LibraryThing
import utils

stub = Adaptor().dump('')
classes = [LiveLib, Amazon, OpenLibrary, Labirint, IQBuy, ISBNDb, LibraryThing]
names = map(lambda a: a().name, classes)
