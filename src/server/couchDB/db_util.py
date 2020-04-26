import couchdb
from datetime import datetime

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
    
    def getkeys(self):
        keys = [id in self.db]
        return keys

    def twput(self, data):
        """save a twitter json document to couchdb

        Arguments:
            data {json} -- twitter file, containing "id_str"
        """
        _id = data["id_str"]
        data["_id"] = _id
        #data["ref_timestamp"] = datetime.now().strftime('%Y%m%d%H%M%S.%f')[:-7]
        try:
            self.db.save(data)
            print(f"...save twitter {_id}")
        except couchdb.http.ResourceConflict:
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
            #data["ref_timestamp"] = datetime.now().strftime('%Y%m%d%H%M%S.%f')[:-7]
        try:
            self.db.save(data)
        except couchdb.http.ResourceConflict:
            _rev = self.db[key]["_rev"]
            data["_rev"] = _rev
            self.db.save(data)
            print(f'...update data {key}')

    def get(self, key):
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

    

    def query(self, mapfunc, reducefunc=None):
        return self.db.query(mapfunc, reducefunc)


    
if __name__ == '__main__':
    
    import json
    twitterdata = json.loads('{"id_str":"1252949121519906816","type":"twitter", "text":"I#newthingfortheday"}')
    normaldata = json.loads('{"type":"AURIN", "purpose":"sample", "version":"2"}')

    db = cdb('http://admin:admin1234@localhost:5984', 'testdb')
    db.twput(twitterdata)

    """
    map_fun = '''function(doc) {
        if (doc.lang == 'en')
        emit(doc.id_str, 1);
        }'''
    for row in db.query(map_fun):
        print(row)
    """