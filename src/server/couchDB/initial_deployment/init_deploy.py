"""
Initial Deployment for couchdb
Running only once after couchdb is set up

"""
import couchdb
import json
import argparse
import os 

# parse arugments
parser = argparse.ArgumentParser(description="set up couchdb")
parser.add_argument('-u', '--username', required=False, help='username')
parser.add_argument('-p', '--password', required=False, help='password')
parser.add_argument('-s', '--server', required=False, help='server url')

serverURL = parser.parse_args().server
username = parser.parse_args().username
password = parser.parse_args().password

#connect to couchdb 
url = 'http://{}:{}@{}:5984/'.format(username,password,serverURL)
connected = False
couchserver = couchdb.Server(url)
try:
    print(f'connected to {couchserver}: {couchserver.version()}')
    connected = True
except ConnectionRefusedError:
    print(f'Connection refused by {url}')

dbs = ['analysis_results','aurin','tweets_mixed']

if connected:
    # create databases
    for db in dbs:
        try:
            couchserver.create(db)
            print(f'database created: <{db}>')
        except ConnectionRefusedError:
            print('Connection refused')
        except Exception:
            print(f'database <{db}> already exists')
        

    # save map_reduce views
    dir_path = os.path.dirname(os.path.realpath(__file__))
    mapreduce_dir = os.path.join(dir_path,'design_cities.json')
    mapreduce_doc = json.load(open(mapreduce_dir,'r'))
    map_dbs = ['tweets_mixed']
    for db in map_dbs:
        couchdb = couchserver[db]
        try:
            if '_rev' in mapreduce_doc:
                del mapreduce_doc['_rev']
            
            couchdb.save(mapreduce_doc)
            print(f'design/cities view is created in <Database {db}>')
        except Exception:
            _rev = couchdb['_design/cities']["_rev"]
            mapreduce_doc["_rev"] = _rev
            couchdb.save(mapreduce_doc)
            print(f'design/cities view is updated in <Database {db}>')

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
            print(f'save {filename} to {couchdb}')
        except Exception:
            key = data['_id']
            _rev = couchdb[key]["_rev"]
            data["_rev"] = _rev
            couchdb.save(data)
            print(f'udpate {filename} to <DATABASE {couchdb}')

    # save aurin data
    couchdb = couchserver['aurin']
    aurin_dir = os.path.join(dir_path,'aurin/')
    for filename in os.listdir(aurin_dir):
        aurinfilename = os.path.join(aurin_dir,filename)
        datafile = open(aurinfilename,'r')
        data = json.load(datafile)
        datafile.close()

        if '_rev' in data:
            del data['_rev']
        try:
            couchdb.save(data)
            print(f'save {filename} to <DATABASE {couchdb}')
        except Exception:
            key = data['_id']
            _rev = couchdb[key]["_rev"]
            data["_rev"] = _rev
            couchdb.save(data)
            print(f'udpate {filename} to {couchdb}')