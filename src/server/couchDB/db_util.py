import couchdb
import time

class cdb:
    def __init__(self, serverURL='http://admin:admin1234@localhost:5984',dbname=None):
        self.serverURL = serverURL
        self.couchserver = couchdb.Server(self.serverURL)
        if dbname is not None:
            self.db=self.couchserver[dbname]
        else:
            self.db = None
    
    def createDB(self, dbname):
        if dbname in self.couchserver:
            print(f"Database {dbname} already exists ")
        else:
            self.couchserver.create(dbname)
    
    def deleteDB(self, dbname):
        try:
            del couchserver[dbname]
        except NameError:
            print(f"Database {dbname} does not exists")

    def showDBs(self):
        dbs = [dbname for dbname in self.couchserver]
        print(dbs)

    def connectDB(self, dbname):
        self.db=self.couchserver[dbname]
    
    def showcurrentDB(self):
        print(self.db)

    def getkeys(self):
        keys = [id in self.db]
        return keys

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
            startkey = [start_ts]
            endkey = [end_ts,{}]
        else:
            startkey = [start_ts,cityname]
            endkey = [end_ts,cityname]
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

    def getview(self, viewname, key=None, include_docs=False, skip=0, reduce=True,group_level=1):
        return self.db.view(viewname, reduce=True,group_level=1)

    def info(self, target):
        print(self.db.info(target))

    
if __name__ == '__main__':
    
    import json
    serverURL = 'http://admin:admin1234@172.26.130.149:5984/'
    dbname = 'tweets_for_test'
    db = cdb(serverURL, dbname)

    #db.showcurrentDB()

    ts0 = int(time.time())
    ts = str(int(time.time()/100)) +'00'

    print("1588261100")
    print(ts0)
    print(ts)

    #for item in db.testview("cities/get_id"):
    #    print(item.doc["place"])
    #    break

    #sydtweets = db.getByCity("Sydney")
    #print(len(sydtweets))
    