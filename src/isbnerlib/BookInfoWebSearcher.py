#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SearchAdaptors

class BookInfoWebSearcher():
    def __init__( self ):
        self.providers = []
        self.providers.append( { "searcher" : SearchAdaptors.LabirintWebSearchAdaptor() } )
        self.providers.append( { "searcher" : SearchAdaptors.IQBuyWebSearchAdaptor() } )
        self.providers.append( { "searcher" : SearchAdaptors.ISBNDbWebSearchAdaptor() } )
        self.providers.append( { "searcher" : SearchAdaptors.LiveLibWebSearchAdaptor() } )

    def getInfo( self, isbn ):
        result = {}

        for provider in self.providers:
            try:
                result = provider["searcher"].getInfo( isbn )
                if "Title" in result and result["Title"]:
                    break
            except:
                pass

        return result

def main():
    masterList = [
            "testtesttest0",
            "9780136006633",
            "9780262162098",
            "9780262062794",
            "9780201914658",
            "9785898155049",
            "9780586087077",
            "9780691127422",
            "9780671657130",
            "9780743276641",
            "9780553380163",
            "9780521644082",
            "9780262220699",
            "9781558601918",
            "9785981440892",
            "9785379003067",
            "9785379011840",
            "9785379003050",
            "9785946480017",
            "9785946480239",
            "9785845908872",
            "9780521785723",
            "9785889344339",
            "5966001855",
            "9785699148653",
        ]

    vasyaList = [
            "9780373228508",
            "9780778320210",
            "9780553271577",
            "9780425132883",
            "9780671534714",
            "9780553279375",
       ]

    imageList = [
            "9780586087077",
            "9780691127422",
            "9780671657130",
            "9785889344339",
            "5966001855",
        ]

    testList = [
            "0679776443",
            "0553095234",
            "5224032490",
        ]

    testList2 = [
            "9781558601918",
            "9780136006633",
            "0521545668",
            "0882332104"
        ]

    searcher = BookInfoWebSearcher()

    for el in masterList:
        print "%s:" % ( el, ),
        info = searcher.getInfo( el )
        print "[%s]" % ( info["Title"], ),

if __name__ == '__main__':
    main()
