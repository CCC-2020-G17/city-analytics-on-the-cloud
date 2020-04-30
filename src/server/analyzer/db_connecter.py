import os
import functools
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
        city_key = city
        return  db.getByCity(city_key)

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

    def __init__(self, city=None):
        self.serverURL = _couchdb_get_url()
        self.city = city

    def save_analysis(self, analysis_result):
        db = db_util.cdb(self.serverURL, "analysis_results_for_test")  # TODO: Change back to analysis_results
        analysis_city_id = "{}_analysis_result".format(self.city.lower())
        db.put(analysis_result, analysis_city_id)

    def update_helper(self, renewal, existing):
        if not isinstance(renewal, dict) or not isinstance(existing, dict):
            if isinstance(renewal, str) and isinstance(existing, str):
                return existing
            elif isinstance(renewal, int) and isinstance(existing, int):
                return renewal + existing
        for key in existing:
            if key in renewal:
                renewal[key] = self.update_analysis(renewal[key], existing[key])
            else:
                renewal[key] = existing[key]
        return renewal

    def update_analysis(self, renewal, existing):
        """
        Add the new result to the existing result. May update only some scenarios.
        :param renewal:
        :return:
        """
        new_result = self.update_helper(renewal, existing)
        self.save_analysis(new_result)


if __name__ == '__main__':
    data_loader = dataLoader('melbourne')
    analysis_result = data_loader.load_analysis()
    result_saver = analysisResultSaver('melbourne')
    result_saver.update_analysis(analysis_result, analysis_result)

