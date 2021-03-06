""" Descriptions    : couchdb utilities to save and fetch data from couchDB
    Project         : COMP90024 Group Project g17
    Author          : Rongbing Shan
"""
import couchdb
import time

class cdb:
    def __init__(self, serverURL='http://cccg17:cccg17@localhost:5984',dbname=None):
        """initialize a CouchDB connection

        Keyword Arguments:
            serverURL {string} -- the server URL (default: {'http://cccg17:cccg17@localhost:5984'})
            dbname {string} -- the db to connect to (default: {None})
        """
        self.serverURL = serverURL
        self.couchserver = couchdb.Server(self.serverURL)
        if dbname is not None:
            self.db=self.couchserver[dbname]
        else:
            self.db = None
    
    def createDB(self, dbname):
        """create a database in couchdb server

        Arguments:
            dbname {string} -- database name to create
        """
        if dbname in self.couchserver:
            print(f"Database {dbname} already exists ")
        else:
            self.couchserver.create(dbname)
    
    def deleteDB(self, dbname):
        """delete a database from couchdb server

        Arguments:
            dbname {string} -- database name to delete
        """
        try:
            del self.couchserver[dbname]
        except NameError:
            print(f"Database {dbname} does not exists")

    def showDBs(self):
        """show all available databases in couch server connected
        """
        dbs = [dbname for dbname in self.couchserver]
        print(dbs)

    def connectDB(self, dbname):
        """connect to specific database for document operations

        Arguments:
            dbname {string} -- database name to connect
        """
        self.db=self.couchserver[dbname]
    
    def showcurrentDB(self):
        """show the database name that is connected
        """
        print(self.db)

    def twput(self, data):
        """save a twitter json document to couchdb

        Arguments:
            data {json} -- twitter file, containing "id_str"
        """
        if "id_str" not in data:
            print("function [twput] require input data contain field 'id_str'")
        else:
            if "_rev" in data:
                del data["_rev"]
            _id = data["id_str"]
            data["_id"] = _id
            data["db_timestamp"] = str(int(time.time()/100)) +'00'
            try:
                self.db.save(data)
                print(f'...save twitter {_id}')
            except couchdb.http.ResourceConflict:
                print(f'...twitter {_id} already in db')
                pass

    
    def put(self, data, key=None):
        """save data of any format to couchdb

        Arguments:
            data {json} -- data to save to couchdb

        Keyword Arguments:
            key {string} -- user specified key for couchdb (default: {None})
        """
        if key is not None:
            data["_id"] = key
            data["db_timestamp"] = str(int(time.time()/100)) +'00'
        try:
            self.db.save(data)
            print(f'...save data {key}')
        except couchdb.http.ResourceConflict:
            _rev = self.db[key]["_rev"]
            data["_rev"] = _rev
            self.db.save(data)
            print(f'...update data {key}')

    def getByKey(self, key):
        """get a document by its key

        Arguments:
            key {[string]} -- [document key]

        Returns:
            [json] -- [document]
        """
        try:
            return self.db[key]
        except couchdb.http.ResourceNotFound:
            print(f'Error: No item found with key{key}')
            return None

    def getAll(self, include_docs=True,skipnum=0):
        """get all documents in a database

        Keyword Arguments:
            include_docs {bool} -- if documents are included (default: {True})
            skipnum {int} -- number of documents to skip (default: {0})

        Returns:
            list -- list of documents
        """
        data = []
        if include_docs:
            for item in self.db.view('_all_docs',include_docs=True,skip=skipnum):
                data.append(item['doc'])
        else:
            for item in self.db.view('_all_docs',include_docs=False, skip=skipnum):
                data.append(item.key)
        return data

    def getByCity(self, cityname):
        """return all documents by city

        Arguments:
            cityname {string} -- city name to look at

        Returns:
            {list} -- a list of twitter documents
        """
        data = []
        for item in self.db.view('cities/by_city',reduce=False,include_docs=True, key=cityname):
            data.append(item.doc)
        return data
        
    def getByBlock(self,start_ts, end_ts, cityname=None, only_id=False):
        """return documents between start and end timestamp for a specific city

        Arguments:
           start_ts {int} -- search start timestamp
          end_ts {int} -- search end timestamp
          cityname {string} -- city to search, default search for all cities
        """
        data = []

        # define start and end key for search
        if cityname is None:
            startkey = [str(start_ts)]
            endkey = [str(end_ts),{}]
        else:
            startkey = [str(start_ts),cityname]
            endkey = [str(end_ts),cityname]
        # whether to include doc or just get id
        if only_id:
            for item in self.db.view('cities/by_ts_city',\
            reduce=False,include_docs=False,startkey=startkey,endkey=endkey):
                data.append(item.id)
        else:
            for item in self.db.view('cities/by_ts_city',\
            reduce=False,include_docs=True,startkey=startkey,endkey=endkey):
                data.append(item.doc)
        # return results
        return data

    def getResult(self,city,suburb=None,scenario=None):
        """get result from database analysis_results

        Arguments:
            city {string} -- city name to filter

        Keyword Arguments:
            suburb {string} -- suburb to filter (default: {None})
            scenario {string} -- analysis scenario to take (default: {None})

        Returns:
            list -- list of documents
        """
        # Quick changes on scenarios
        CITY_SCENARIOS = ('covid-19','crime')
        SUBUR_SCENARIOS = ('income','education','migration')
        CITIES = ('adelaide','brisbane','melbourne','perth','sydney')

        #check city names
        city = city.lower()
        if city not in CITIES:
            print(f'city must be one of {CITIES}')
            return None
        # define scenarios to take, default as to take all
        if suburb is None:
            scenarios = CITY_SCENARIOS
        else:
            scenarios = SUBUR_SCENARIOS
        if scenario is not None:
            if scenario not in scenarios:
                print(f'please specify a scenario from {scenarios}')
                return None
            else:
                scenarios = [scenario]
        # document key to retrive from
        key = city + '_analysis_result'
        print(f'>>getting data from {key}')
        # prepare data
        data = {}
        doc =  self.db[key]
        # city and all suburbs
        if suburb == 'city&suburb':
            return doc
        # only suburbs
        if suburb == 'all':
            return doc["suburbs"]
        #
        if suburb is not None:
            suburb = suburb.upper()
            data["city_name"] = doc["city_name"]
            data["suburb"] = suburb
            data["suburb_tweet_count"] = doc["suburbs"][suburb.upper()]["suburb_tweet_count"]
            for s in scenarios:
                data[s] = doc["suburbs"][suburb.upper()][s]
            return data
        else:
            data["city_name"] = doc["city_name"]
            data["city_tweet_count"] = doc["city_tweet_count"]
            data["city_tweet_with_geo_count"] = doc["city_tweet_with_geo_count"]
            data["suburb_tweet_count"] = 0
            for s in scenarios:
                data[s] = doc[s]
            return data
 
    def getResult_listsuburbs(self,city):
        """return all suburbs in db for a city

        Arguments:
            cityname {string} -- city name to look at

        Returns:
            {[string]]} -- a list of suburb names
        """
        suburbs = []
        key = city.lower() + '_analysis_result'
        for suburb in self.db[key]["suburbs"]:
            suburbs.append(suburb)
        return suburbs
    
if __name__ == '__main__':
    pass

