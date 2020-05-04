from flask import Flask, request, url_for
import json
from flask_cors import CORS
from utils import city_info_loader

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/api/statistic', methods=['GET'])
def get_statistic_api():
    # http://0.0.0.0:3000/api/statistic?city=melbourne
    city = request.args.get('city')
    res = {}
    if (city != None):
        res = city_info_loader.safe_load_all_data_of(city)
    return res


@app.route('/api/v2.0/map/city/<string:city>', methods=['GET'])
def get_map(city):
    # http://0.0.0.0:3000/api/v2.0/map/city/melbourne
    return city_info_loader.safe_load_map_of(city)


@app.route('/api/v2.0/analysis/city/<string:city>', methods=['GET'])
def get_city_analysis(city):
    # http://0.0.0.0:3000/api/v2.0/analysis/city/melbourne
    return city_info_loader.safe_load_city_analysis_of(city)


@app.route('/api/v2.0/analysis/suburbs-of-city/<string:city>', methods=['GET'])
def get_suburbs_analysis(city):
    # http://0.0.0.0:3000/api/v2.0/analysis/suburbs-of-city/melbourne
    return city_info_loader.safe_load_suburbs_analysis_of(city)


@app.route('/api/v2.0/data/<string:city>', methods=['GET'])
def get_all_data(city):
    # http://0.0.0.0:3000/api/v2.0/data/melbourne
    return city_info_loader.safe_load_all_data_of(city)


def testAPI():
    url1 = '/api/statistic?city=melbourne&suburb=AIRPORT%20WEST'
    url2 = '/api/v2.0/map/city/melbourne'
    with app.test_request_context(url1):
        city = request.args.get('city')
        suburb = request.args.get('suburb')
        print(city, suburb)


if __name__ == '__main__':
    app.run(debug=False, port=3000, host='0.0.0.0')
