import couchdb
import time

class cdb:
    def __init__(self, serverURL='http://admin:admin1234@localhost:5984',dbname=None):
        """initialize a CouchDB connection

        Keyword Arguments:
            serverURL {string} -- the server URL (default: {'http://admin:admin1234@localhost:5984'})
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
            del couchserver[dbname]
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
        try:
            return self.db[key]
        except couchdb.http.ResourceNotFound:
            print(f'Error: No item found with key{key}')
            return None

    def getAll(self, include_docs=True,skipnum=0):
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
        for item in self.db.view('cities/get_id',include_docs=True, key=cityname):
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
            for item in self.db.view('cities/get_timestamp',\
            reduce=False,include_docs=False,startkey=startkey,endkey=endkey):
                data.append(item.id)
        else:
            for item in self.db.view('cities/get_timestamp',\
            reduce=False,include_docs=True,startkey=startkey,endkey=endkey):
                data.append(item.doc)
        # return results
        return data

    def getResult(self,scenario,city,suburb=None):
        city = city.lower()
        cities = ('adelaide','brisbane','melbourne','perth','sydney')
        scenarios = ('covid-19','crime','income','education','migration')
        if scenario not in scenarios:
            print(f'scenarios must be one of {scenarios}')
            return None
        if city not in cities:
            print(f'city must be one of {cities}')
            return None

        key = city + '_analysis_result'
        print(f'>>getting data from {key}')
        doc =  self.db[key]
        if suburb is not None:
            suburb = suburb.upper()
            data = {}
            if scenario == 'crime' or scenario == 'covid-19':
                print(f'there is no data of {scenario} in {suburb}')
                return None
            else:
                data["city_name"] = doc["city_name"]
                data["suburb"] = suburb
                data["suburb_tweet_count"] = doc["suburbs"][suburb.upper()]["suburb_tweet_count"]
                data[scenario] = doc["suburbs"][suburb.upper()][scenario]
                return data
        else:
            data = {}
            data["city_name"] = doc["city_name"]
            data["city_tweet_count"] = doc["city_tweet_count"]
            data["city_tweet_with_geo_count"] = doc["city_tweet_with_geo_count"]
            data["suburb_tweet_count"] = 0

            if scenario == 'crime' or scenario == 'covid-19':
                data[scenario] = doc[scenario]
                return data
            else:
                print(f'{scenario} is suburb level, please specify the suburb')
                return None
            """
                for sub in doc["suburbs"]:
                    data["suburb_tweet_count"] += doc["suburbs"][sub]["suburb_tweet_count"]
                    for item in doc["suburbs"][sub][scenario]:
                        if item not in data:
                            data[item] = doc["suburbs"][sub][scenario][item]
                        else:
                            data[item] += doc["suburbs"][sub][scenario][item]
                return data
            """

    """
    def getkeys(self):
        keys = [id in self.db]
        return keys

    def getview(self, viewname, key=None, include_docs=False, skip=0, reduce=True,group_level=1):
        return self.db.view(viewname, reduce=True,group_level=1)

    def info(self, target):
        print(self.db.info(target))
    """
    
if __name__ == '__main__':
    
    serverURL = 'http://admin:admin1234@172.26.130.149:5984/'
    dbname = 'analysis_results'
    db = cdb(serverURL, dbname)

    db.showcurrentDB()

    print(db.getResult('income','adelaide','rOYSTON PARK'))
