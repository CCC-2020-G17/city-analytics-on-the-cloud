import json
import db_util
import argparse

parser = argparse.ArgumentParser(description="write twitter from json file to couchDB")
parser.add_argument('-s', '--server', required=False, help='server url')
parser.add_argument('-db', '--dbname', required=True, help='database name')

serverURL = parser.parse_args().server
dbname = parser.parse_args().dbname

if serverURL == None:
    serverURL = "http://admin:admin1234@localhost:5984/"

print(f"ready to read from {serverURL}{dbname}")

print(serverURL)
db = db_util.cdb(serverURL)
db.connectDB(dbname)
data = db.getAll()

print(f'number of documents fetched: {len(data)}')