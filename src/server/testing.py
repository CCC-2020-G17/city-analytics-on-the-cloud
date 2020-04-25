import couchdb
import json

user = "admin"
password = "admin1234"
couchserver = couchdb.Server("http://%s:%s@172.26.130.149:5984/" % (user, password))
#couchserver = couchdb.Server("http://localhost:5984")

db = couchserver['twitters']

for docid in db.view('_all_docs',include_docs=True):
    print(docid['doc'])
    break