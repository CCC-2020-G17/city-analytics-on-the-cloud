import os
from couchDB import db_util
from configparser import ConfigParser

def _couchdb_get_url(section='DEFAULT', verbose=False):
    global config
    config = ConfigParser()
    url_file = '{}/config/server.url.cfg'.format(os.path.pardir)
    if verbose:
        print('url_file {}'.format(url_file))
    config.read(url_file)
    server_url = config.get(section, 'server_url')
    return server_url


class dataLoader():

    def __init__(self, city=None):
        self.serverURL = _couchdb_get_url()
        self.city = city

    def load_tweet_data(self, city):
        # TODO: MapReduce to get data only from the specified city and specified queries.
        db = db_util.cdb(self.serverURL, "tweets_for_test")
        return db.getAll()

    def load_city_suburb_coordinates(self):
        if self.city:
            city_key = "{}_suburbs".format(self.city.lower())
            db = db_util.cdb(self.serverURL, "aurin")
            return db.getByKey(city_key)
        else:
            return None

    def load_analysis(self):
        if self.city:
            db = db_util.cdb(self.serverURL, "analysis_results_for_test")
            city_key = "{}_analysis_result".format(self.city.lower())
            return db.getByKey(city_key)
        else:
            return None


class analysisResultSaver():

    def __init__(self, city):
        self.serverURL = _couchdb_get_url()
        self.city = city

    def save_analysis(self, analysis_result):
        db = db_util.cdb(self.serverURL, "analysis_results_for_test")  # TODO: Change back to analysis_results
        analysis_city_id = "{}_analysis_result".format(self.city.lower())
        db.put(analysis_result, analysis_city_id)

    def update_analysis(self, analysis_result):
        """
        Add the new result to the existing result. May update only some scenarios.
        :param analysis_result:
        :return:
        """
        pass
