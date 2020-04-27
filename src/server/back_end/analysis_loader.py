from couchDB import db_util
from configparser import ConfigParser

def _couchdb_get_url(section='DEFAULT', verbose=False):
    global config
    config = ConfigParser()
    url_file = 'config/server.url.cfg'
    if verbose:
        print('url_file {}'.format(url_file))
    config.read(url_file)
    server_url = config.get(section, 'server_url')
    return server_url

def load_city_analysis(city):
    """
    Load analysis result for specified city in JSON format.
    :param city: string city name
    :return: JSON city analysis result
    """
    server_url = _couchdb_get_url()
    city_key = "{}_analysis_result".format(city.lower())
    try:
        db = db_util.cdb(server_url, "analysis_results")
        return db.get(city_key)
    except Exception as e:
        raise e