import couchdb
import requests

serverurl = "http://admin:admin1234@localhost:5984/"
dbname = "tweets_with_geo"

couchserver = couchdb.Server(serverurl)
db = couchserver[dbname]

headers = {'Content-type':'application/json'}
link = "http://admin:admin1234@localhost:5984/{}/_design/insert_ts/_update/insert_ts/{}"

count=0

for item in db.view('_all_docs'):
    url = link.format(dbname,item.id)
    r = requests.put(url,headers=headers)
    count += 1
    print(f'processed {count}')