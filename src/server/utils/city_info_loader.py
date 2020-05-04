import json
import os
from couchDB import db_util
from configparser import ConfigParser

# http://172.26.130.149:5984/_utils/
# admin:admin1234

# ***** Function use to connect with couchdb ***************


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


# def _load_from_db(db_name, key, scenario):
#     server_url = _couchdb_get_url()
#     try:
#         db = db_util.cdb(server_url, db_name)
#         return db.getByKey(key)
#     except Exception as e:
#         return {}

# **********************************************************


def _from_db_load_analysis_of(city):
    return _load_from_db("analysis_results", "{}_analysis_result".format(city))


def _from_db_load_city_analysis_of(city):
    data = _from_db_load_analysis_of(city)
    if 'suburbs' in data:
        del data['suburbs']
    return data


def _from_db_load_suburbs_analysis_of(city):
    data = _from_db_load_analysis_of(city)
    return data['suburbs']


def _from_db_load_map_of(city):
    return _load_from_db("aurin", "{}_suburbs".format(city))


def _load_all_data_of(city):
    # Mearge the map info with analysis data
    data = _from_db_load_map_of(city)
    analysis_data = _from_db_load_analysis_of(city)
    for suburb in data['features']:
        try:
            suburb_name = suburb['properties']['name']
            suburb_analysis = analysis_data['suburbs'][suburb_name]
            suburb['properties']['analysis_result'] = suburb_analysis
        except Exception as e:
            # Ignore but print the error
            print('Error from utils/city_info_loader.py: ', e)
    if 'suburbs' in analysis_data:
        del analysis_data['suburbs']
    data['analysis_result'] = analysis_data
    return data


def _is_city_valid(city):
    # Current available city: "Melbourne", "Sydney", "Brisbane", "Adelaide", "Perth"
    valid_city = {"melbourne", "sydney", "brisbane", "adelaide", "perth"}
    return city in valid_city


def _load_with_check(city, func):
    res = {}
    city = city.lower()
    if _is_city_valid(city):
        res = func(city)
    return res

# *************** Public ************************************


def safe_load_map_of(city):
    return _load_with_check(city, _from_db_load_map_of)


def safe_load_city_analysis_of(city):
    return _load_with_check(city, _from_db_load_city_analysis_of)


def safe_load_suburbs_analysis_of(city):
    return _load_with_check(city, _from_db_load_suburbs_analysis_of)


def safe_load_all_data_of(city):
    """
    Load city information with both geographic information and analysis
    :param string City name (Melbourne, Sydney, Brisbane, Adelaide, Perth)
    :return dict City information
    """
    return _load_with_check(city, _load_all_data_of)
