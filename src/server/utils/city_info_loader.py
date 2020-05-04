import json
import os
from couchDB import db_util
from configparser import ConfigParser

# http://172.26.130.149:5984/_utils/
# admin:admin1234

def _couchdb_get_url(section='DEFAULT', verbose=False):
    config = ConfigParser()
    url_file = 'config/server.url.cfg'
    if verbose:
        print('url_file {}'.format(url_file))
    config.read(url_file)
    server_url = config.get(section, 'server_url')
    return server_url

def _load_from_db(db_name, key):
    server_url = _couchdb_get_url()
    try:
        db = db_util.cdb(server_url, db_name)
        return db.getByKey(key)
    except Exception as e:
        return {}
        # raise e

def _load_city_analysis_from_db(city):
    return _load_from_db("analysis_results", "{}_analysis_result".format(city))

def _load_city_geoinfo_from_db(city):
    return _load_from_db("aurin", "{}_suburbs".format(city))

def _is_city_valid(city):
    # Current available city: "Melbourne", "Sydney", "Brisbane", "Adelaide", "Perth"
    valid_city = {"melbourne", "sydney", "brisbane", "adelaide", "perth"}
    return city in valid_city

def _get_merge_data(city):
    data = _load_city_geoinfo_from_db(city)
    analysis_data = _load_city_analysis_from_db(city)
    for suburb in data['features']:
        try:
            suburb_name = suburb['properties']['name']
            suburb_analysis = analysis_data['suburbs'][suburb_name]
            suburb['properties']['analysis_result'] = suburb_analysis
        except Exception as e:
            # Ignore but print the error
            print('Error from utils/city_info_loader.py: ', e)
    return data

def load_city_info(city):
    """
    Load city information with both geographic information and analysis
    :param string City name (Melbourne, Sydney, Brisbane, Adelaide, Perth)
    :return dict City information
    """
    res = {}
    city = city.lower()
    if _is_city_valid(city):
        res = _get_merge_data(city)
    return res

def load_suburb_info(city, suburb):
    """
    Load city information with both geographic information and analysis
    :param string City name (Melbourne, Sydney, Brisbane, Adelaide, Perth)
    :param string Suburb name
    :return dict Suburb information
    """
    city = city.lower()
    suburb = suburb.lower()
    city_info = load_city_info(city)
    for suburb in city_info['features']:
        if suburb['properties']['name'] == suburb:
            return suburb
    return {}



