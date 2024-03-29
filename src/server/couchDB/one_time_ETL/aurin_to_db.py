import os
import json
import re
import db_util

COUCHDB_URL = 'http://{}:{}@{}:{}/'
COUCHDB_DOMAIN = '172.26.130.149'
COUCHDB_USERNAME = 'admin'
COUCHDB_PASSWORD = 'admin1234'
COUCHDB_PORTS = 5984
DBNAME = 'aurin'

db = db_util.cdb(COUCHDB_URL.format(COUCHDB_USERNAME,COUCHDB_PASSWORD,COUCHDB_DOMAIN,COUCHDB_PORTS), DBNAME)

db.showcurrentDB()

dirpath = './aurin_data/'
for filename in os.listdir(dirpath):
    content = open(os.path.join(dirpath,filename),'r')
    data = json.load(content)
    _id = filename[:-5]
    
    if filename.endswith('_suburbs.json'):
        #db.put(data,_id)
        pass
    elif filename.endswith('_demographics.json'):
        print(f'save {filename} to {db}')
        data_toload = {}
        data_toload["_id"] = _id
        data_toload["features"] = {}
        for item in data['features']:
            region = item['properties']['gccsa_name_2011']
            regiondata = item['properties']
            regiondata["id"]=item["id"]
            data_toload["features"][region] = regiondata
        db.put(data_toload,_id)
    elif filename.endswith('_languages.json'):
        print(f'save {filename} to {db}')
        data_toload = {}
        data_toload["_id"] = _id
        data_toload["features"] = {}
        for item in data['features']:
            region = item['properties']['gcc_name16']
            regiondata = item['properties']
            regiondata["id"]=item["id"]
            data_toload["features"][region] = regiondata
        db.put(data_toload,_id)
    else:
        data_toload = {}
        data_toload["_id"] = _id
        data_toload["suburbs"] = {}
        i = 1
        for item in data['features']:
            suburb_oriname = item['properties']['sa2_name16']
            suburbnamelist = suburb_oriname.replace('Yarra -', 'Yarra').split('-')
            suburbdata = item['properties']
            del suburbdata['sa2_name16']
            for suburbname in suburbnamelist:
                suburbname = re.sub(r" ?\([^)]+\)", "", suburbname)
                suburbname = suburbname.strip().upper()
                data_toload['suburbs'][suburbname] = suburbdata
                #print(f'{suburb_oriname} ---> {suburbname}')
        db.put(data_toload,_id)