# -*- coding: utf-8 -*-

from adaptor import Adaptor
from amazon import Amazon
from livelib import LiveLib
from openlibrary import OpenLibrary
from labirint import Labirint
from iqbuy import IQBuy
from isbndb import ISBNDb
import utils
import pyisbn

stub = Adaptor().dump('')
classes = [LiveLib, Amazon, OpenLibrary, Labirint, IQBuy, ISBNDb]
names = map(lambda a: a().name, classes)
