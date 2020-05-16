import cloudant
import time

class cdb:
    def __init__(self, username='admin',password='admin1234',serverURL='http://localhost:5984',dbname=None):
        self.serverURL = serverURL
        self.couchserver = cloudant.client.CouchDB(username,password,url=serverURL,connect=True)
        if dbname is not None:
            self.db=self.couchserver[dbname]
        else:
            self.db = None

    def showDBs(self):
        dbs = [dbname for dbname in self.couchserver]
        print(dbs)

    def connectDB(self, dbname):
        self.db=self.couchserver[dbname]
    
    def showcurrentDB(self):
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
            data["ref_timestamp"] = str(int(time.time()))
            try:
                self.db.create_document(data,throw_on_exists=True)
                print(f'...save twitter {_id}')
            except cloudant.error.CloudantDatabaseException:
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
            data["ref_timestamp"] = str(int(time.time()))
        try:
            self.db.create_document(data,throw_on_exists=True)
        except cloudant.error.CloudantDatabaseException:
            _rev = self.db[key]["_rev"]
            data["_rev"] = _rev
            self.db.create_document(data,throw_on_exists=True)
            print(f'...update data {key}')

    def getByKey(self, key):
        try:
            return self.db[key]
        except couchdb.http.ResourceNotFound:
            print(f'Error: No item found with key{key}')
            return None

    def getAll(self):
        data = []
        for item in self.db.view('_all_docs',include_docs=True):
            data.append(item['doc'])
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

    def query(self, mapfunc, reducefunc=None):
        return self.db.query(mapfunc, reducefunc)
    def testview(self, viewname):
        return self.db.view(viewname,include_docs=True, key="Sydney")
    def info(self, target):
        print(self.db.info(target))

    
if __name__ == '__main__':
    
    db = cdb(dbname='testdb')
    data = {"id_str":"test1", "content": "no"}
    db.put(data,"test1")
    