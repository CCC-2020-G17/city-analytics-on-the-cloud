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


"""sample6 fetch data by timestamp and city"""
# required views to be created in db in advance
# start and end timestamp can be the same, cityname can be empty to search for all twitters,\
#       even if [doc.place] is empty
cityData = db.getByBlock(start_ts='1588261100',end_ts='1588261100',cityname='Sydney')
cityData = db.getByBlock(start_ts='1588261100',end_ts='1588261100') # search for all twitters ignore city information


""" sample7, get analysis results"""
serverURL = 'http://admin:admin1234@172.26.130.149:5984/'
dbname = 'analysis_results'
db = db_util.cdb(serverURL, dbname)
# get data by scenario
data1 = db.getResult(city='adelaide',scenario='crime')  # get city data for specified scenario
data2 = db.getResult(city='adelaide',suburb='ROYSTON PARK',scenario='income') # get suburb data of specified scenario
# get data of all scenario of city or suburb
data3 = db.getResult(city='adelaide',suburb='ROYSTON PARK') # get suburb data of all scenarios
data4 = db.getResult(city='adelaide')  # get city data of all scenarios
# get all data of suburbs under a city - no city data included
data5 = db.getResult(city='adelaide',suburb='all') # retrive all data of a city
# get all data of a city, include city data
data5 = db.getResult(city='adelaide',suburb='city&suburb') # retrive all data of a city
""" sample8, get all suburbs in db under a city"""
print(db.getResult_listsuburbs('adelaide'))


"""how to use json_to_db"""
#python3 json_to_db.py -f [json file name] -s [serverURL] -db [dbname]
#below command can be run when VPN connected, from local machine
## python3 json_to_db.py -f tinyData.json -s http://admin:admin1234@172.26.130.149:5984/ -db twitters
