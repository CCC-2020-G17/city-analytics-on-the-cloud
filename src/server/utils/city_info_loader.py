import json
import os
from couchDB import db_util
from configparser import ConfigParser

# http://172.26.130.149:5984/_utils/
# admin:admin1234

# *************** Public ************************************
def get_valid_cities():
    """
    Get all the cities that is available in the database
    :return cities' names
    """
    return _valid_cities

def safe_load_map_of(city):
    """
    Load city map info
    :param string City name
    :return dict City map info
    """
    return _load_with_check(city, _from_db_load_map_of)


def safe_load_city_analysis_of(city):
    """
    Load city-level analysis
    :param string City name
    :return dict city-level analysis
    """
    return _load_with_check(city, _from_db_load_city_analysis_of)


def safe_load_suburbs_analysis_of(city):
    """
    Load Suburb-level analysis of a specific city
    :param string City name
    :return dict Suburb-level analysis, contain analysis of all the suburbs in the city.
    """
    return _load_with_check(city, _from_db_load_suburbs_analysis_of)


def safe_load_all_data_of(city):
    """
    Load city information with both geographic information and analysis
    :param string City name (Melbourne, Sydney, Brisbane, Adelaide, Perth)
    :return dict City information
    """
    return _load_with_check(city, _load_all_data_of)


def safe_load_all_cities_analysis():
    """
    Load all the cities' analysis without suburbs analysis. (City-level Data)
    :return dict City information
    """
    res = {}
    for city in _valid_cities:
        res[city] = _from_db_load_city_analysis_of(city)
    return res

def safe_load_all_analysis():
    """
    Load all the analysis
    :return dict City information
    """
    res = {}
    for city in _valid_cities:
        res[city] = _from_db_load_analysis_of(city)
    return res


# ***** Function use to connect with couchdb ***************

def _couchdb_get_url(section='DEFAULT', verbose=False):
    """ Get the url of the couchdb """
    config = ConfigParser()
    url_file = 'config/server.url.cfg'
    if verbose:
        print('url_file {}'.format(url_file))
    config.read(url_file)
    server_url = config.get(section, 'server_url')
    return server_url


def _load_from_db(db_name, key):
    """ Load data from the couchdb """
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

# ******************** Private *********************************

# The cities that is available in the database
_valid_cities = {"melbourne", "sydney", "brisbane", "adelaide", "perth"}

def _from_db_load_analysis_of(city):
    """Load all analysis of a city"""
    return _load_from_db("analysis_results", "{}_analysis_result".format(city))


def _from_db_load_city_analysis_of(city):
    """Load only city-level analysis of a city without suburbs analysis"""
    data = _from_db_load_analysis_of(city)
    if 'suburbs' in data:
        del data['suburbs']
    return data


def _from_db_load_suburbs_analysis_of(city):
    """ Load analysis of a specific suburbs """
    data = _from_db_load_analysis_of(city)
    return data['suburbs']


def _from_db_load_map_of(city):
    """ Load the map of a specific city """
    return _load_from_db("aurin", "{}_suburbs".format(city))


def _load_all_data_of(city):
    """ Load both the map data and the analysis of a specific """
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
    """ Check if the city is available in the database """
    return city in _valid_cities


def _load_with_check(city, func):
    """ Run with city valid check """
    res = {}
    city = city.lower()
    if _is_city_valid(city):
        res = func(city)
    return res
