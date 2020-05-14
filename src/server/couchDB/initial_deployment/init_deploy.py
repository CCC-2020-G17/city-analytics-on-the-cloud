"""
Initial Deployment for couchdb
Running only once after couchdb is set up
"""
import couchdb
import json
import argparse
import os 


parser = argparse.ArgumentParser(description="set up couchdb")
parser.add_argument('-u', '--username', required=False, help='username')
parser.add_argument('-p', '--password', required=False, help='password')
parser.add_argument('-s', '--server', required=False, help='server url')

serverURL = parser.parse_args().server
username = parser.parse_args().username
password = parser.parse_args().password

url = 'http://{}:{}@{}:5984/'.format(username,password,serverURL)

couchserver = couchdb.Server(url)
print(f'connected to {url}')

dbs = ['analysis_results','aurin','tweets_for_test','tweets_mixed','tweets_with_geo','twitters']

# create databases
for db in dbs:
    try:
        couchserver.create(db)
        print(f'database created: <{db}>')
    except Exception:
        print(f'database <{db}> already exists')
    

# save map_reduce views
dir_path = os.path.dirname(os.path.realpath(__file__))
mapreduce_dir = os.path.join(dir_path,'design_cities.json')
mapreduce_doc = json.load(open(mapreduce_dir,'r'))
map_dbs = ['tweets_for_test','tweets_mixed','tweets_with_geo','twitters']
for db in map_dbs:
    couchdb = couchserver[db]
    try:
        if '_rev' in mapreduce_doc:
            del mapreduce_doc['_rev']
        
        couchdb.save(mapreduce_doc)
        print(f'design/cities view is created in <{db}>')
    except Exception:
        _rev = couchdb['_design/cities']["_rev"]
        mapreduce_doc["_rev"] = _rev
        couchdb.save(mapreduce_doc)
        print(f'design/cities view is updated in <{db}>')

# save analysis results
analysis_files = ['adelaide_analysis_result.json','brisbane_analysis_result.json',\
    'melbourne_analysis_result.json','perth_analysis_result.json','sydney_analysis_result.json']
couchdb = couchserver['analysis_results']
for filename in analysis_files:
    analysis_file = open(os.path.join(dir_path,filename),'r')
    data = json.load(analysis_file)
    analysis_file.close()
    if '_rev' in data:
        del data['_rev']
    try:
        couchdb.save(data)
        print(f'save {filename} to <{couchdb}>')
    except Exception:
        key = data['_id']
        _rev = couchdb[key]["_rev"]
        data["_rev"] = _rev
        couchdb.save(data)
        print(f'udpate {filename} to <{couchdb}>')

