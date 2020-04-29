""" sample usage on db_util.py
Unimelb vpn required to run the code
Couchdb UI can be accessed through:   http://172.26.130.149:5984/_utils/
username/password: admin/admin1234

to access the CouchDB instance, download couchDB.pem from Slack and run:
ssh -i couchDB.pem ubuntu@172.26.130.149
"""
import db_util
import json
import argparse

serverURL = "http://admin:admin1234@172.26.130.149:5984/"

"""sample1, connect to server without specific database"""
#connect to server with URL
couchserver = db_util.cdb(serverURL)

#create database, if needed
##couchserver.createDB('sample')
#show all databases on server
couchserver.showDBs()

"""sample2 connect to server with specific database
    > recommanded way
"""
db = db_util.cdb(serverURL, "sample")

#sample data of twitter and normal(from AURIN)
#twitter data needs to have field [id_str]
twitterdata = json.loads('{"id_str":"1252949121519906816","type":"twitter", "text":"I#newthingfortheday"}')
normaldata = json.loads('{"type":"AURIN", "purpose":"sample"}')

#write twitterdata, can update duplicate data by id_str
db.twput(twitterdata)

#write AURIN data, cannot distinguish duplicate data
db.put(normaldata)  #without key, system will generate random key in couchdb
db.put(normaldata, 'key1')  #insert/update with key value


"""sample3 fecth all data in a database"""
# data returned is a list
all_data = db.getAll()  #all data is a list containing all documents in the db
print('**** all data****')
for d in all_data:
    print(d)

"""sample4 fetch data by key (for twitters only)"""
# data returned is a json document
one_data = db.getByKey('1252949121519906816')
print('**** one data****')
print(one_data)

"""sample5 fetch twitters of a city"""
# required views to be created in the database in advance.
# returns all twitters of this city in a [list]
cityData = db.getByCity("Sydney")


"""how to use json_to_db"""
#python3 json_to_db.py -f [json file name] -s [serverURL] -db [dbname]
#below command can be run when VPN connected, from local machine
## python3 json_to_db.py -f tinyData.json -s http://admin:admin1234@172.26.130.149:5984/ -db twitters
