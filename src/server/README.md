# API Server

Already connect to db.

## Database Manager
http://172.26.130.149:5984/_utils/



## Quick look:

About how to connect to the remote server:

**API 1.0:**

- http://172.26.130.149:3000/api/statistic?city=melbourne

- http://172.26.130.149:3000/api/statistic?city=sydney

- http://172.26.130.149:3000/api/statistic?city=brisbane

- http://172.26.130.149:3000/api/statistic?city=adelaide

- http://172.26.130.149:3000/api/statistic?city=perth

**API 2.0**

- To get the map:

   http://172.26.130.149:3000/api/v2.0/map/city/melbourne

- To get the analysis of a city: 

  http://172.26.130.149:3000/api/v2.0/analysis/city/melbourne

- To get the analysis of all suburbs in a city: 

  http://172.26.130.149:3000/api/v2.0/analysis/suburbs-of-city/melbourne

- To get all the data about a city *(like the result of API 1.0, but contain the analysis of city)*: 

  http://172.26.130.149:3000/api/v2.0/data/melbourne





## Usage (Local Run)

1. First, make sure you connect to the Unimelb VPN

2. Then use the command shown below to run the server

   ```
   python app.py
   ```

3. And then, you can get the data from:

   **API 1.0:**

   - http://0.0.0.0:3000/api/statistic?city=melbourne

   - http://0.0.0.0:3000/api/statistic?city=sydney

   - http://0.0.0.0:3000/api/statistic?city=brisbane

   - http://0.0.0.0:3000/api/statistic?city=adelaide

   - http://0.0.0.0:3000/api/statistic?city=perth

   **API 2.0**

   - To get the map:

      http://0.0.0.0:3000/api/v2.0/map/city/melbourne

   - To get the analysis of a city: 

     http://0.0.0.0:3000/api/v2.0/analysis/city/melbourne

   - To get the analysis of all suburbs in a city: 

     http://0.0.0.0:3000/api/v2.0/analysis/suburbs-of-city/melbourne

   - To get all the data about a city *(like the result of API 1.0, but contain the analysis of city)*: 

     http://0.0.0.0:3000/api/v2.0/data/melbourne