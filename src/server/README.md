# API Server

No connection with the couchDB currently.



## Usage (Local Run)

1. First, make sure you connect to the Unimelb VPN

2. Then use the command shown below to run the server

   ```
   python app.py
   ```

3. And then, you can get the data from:

   http://0.0.0.0:3000/api/statistic?city=melbourne

   http://0.0.0.0:3000/api/statistic?city=sydney

   http://0.0.0.0:3000/api/statistic?city=brisbane

   http://0.0.0.0:3000/api/statistic?city=adelaide

   http://0.0.0.0:3000/api/statistic?city=perth

4. Or get data from couchDB server
    http://172.26.130.149:3000/api/statistic?city=melbourne

    http://172.26.130.149:3000/api/statistic?city=sydney

    http://172.26.130.149:3000/api/statistic?city=brisbane

    http://172.26.130.149:3000/api/statistic?city=adelaide

    http://172.26.130.149:3000/api/statistic?city=perth