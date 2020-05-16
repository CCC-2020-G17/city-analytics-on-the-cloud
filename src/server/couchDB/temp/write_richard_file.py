import json
import db_util


serverURL = 'http://admin:admin1234@172.26.130.149:5984/'
dbname = 'tweets_with_geo'
db = db_util.cdb(serverURL, dbname)

filename = 'twitter-melb.json'
count = 0
file0 = open(filename,'r')
for line in file0:
    if(line.endswith(',\n')):
        line = line[:-2]
        data = json.loads(line)
        print(data)
        break;
        #if(data['key'][1]==2017):
            #count += 1
            #db.twput(data['doc'])
        
print('total: ', count)


