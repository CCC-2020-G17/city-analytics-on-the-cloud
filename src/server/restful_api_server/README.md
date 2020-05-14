# API Server

Already connect to db.

## Database Manager
http://172.26.130.149:5984/_utils/



## Quick look:

About how to connect to the remote server:

**API 1.0:**

- http://172.26.130.149/api/statistic?city=melbourne

- http://172.26.130.149/api/statistic?city=sydney

- http://172.26.130.149/api/statistic?city=brisbane

- http://172.26.130.149/api/statistic?city=adelaide

- http://172.26.130.149/api/statistic?city=perth

**API 2.0**

- To get the map:

  http://172.26.130.149/api/v2.0/map/city/melbourne

- To get the analysis of a city: 

  http://172.26.130.149/api/v2.0/analysis/city/melbourne

- To get the analysis of all suburbs in a city: 

  http://172.26.130.149/api/v2.0/analysis/suburbs-of-city/melbourne

- To get all the data about a city *(like the result of API 1.0, but contain the analysis of city)*: 

  http://172.26.130.149/api/v2.0/data/melbourne

- **Load all the cities' analysis without suburbs analysis. (City-level Data):**

  http://172.26.130.149/api/v2.0/analysis/city-level/all

- **Get all analysis:**

  http://172.26.130.149/api/v2.0/analysis/suburb-level/all
