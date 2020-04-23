import db_util
import json
import argparse

parser = argparse.ArgumentParser(description="write twitter from json file to couchDB")
parser.add_argument('-f', '--filename', required=True, help='json file name')
parser.add_argument('-s', '--server', required=False, help='server url')
parser.add_argument('-db', '--dbname', required=True, help='database name')

filename = parser.parse_args().filename
serverURL = parser.parse_args().server
dbname = parser.parse_args().dbname

if serverURL == None:
    serverURL = "http://admin:admin1234@localhost:5984/"

print(f"ready to write file from {filename} to {serverURL}-{dbname}")

file0 = open(filename, 'r')
for line in file0:
    data = json.loads(line)
    db = db_util.cdb(serverURL)
    db.connectDB(dbname)
    db.put(data)
file0.close()