import couchdb
COUCHDB_URL = 'http://{}:{}@{}:{}/'
COUCHDB_DOMAIN = '172.26.130.149'
COUCHDB_USERNAME = 'admin'
COUCHDB_PASSWORD = 'admin1234'
COUCHDB_PORTS = 5984
DBNAME = 'tweets_with_geo'
serverURL = COUCHDB_URL.format(COUCHDB_USERNAME,COUCHDB_PASSWORD,COUCHDB_DOMAIN,COUCHDB_PORTS)

couchserver = couchdb.Server(serverURL)
db = couchserver[DBNAME]

print(db)

for item in db.view('users/get_uid',reduce=True,group_level=1):
    print(item.key)
    break;