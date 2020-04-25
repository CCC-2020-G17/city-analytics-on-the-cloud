import json
import db_util
from collections import defaultdict, Counter
# from geotext import GeoText
from configparser import ConfigParser
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def _couchdb_get_url(section='DEFAULT', verbose=False):
    global config
    config = ConfigParser()
    url_file = 'config/server.url.cfg'
    if verbose:
        print('url_file {}'.format(url_file))
    config.read(url_file)
    server_url = config.get(section, 'server_url')
    return server_url


class dataLoader():

    def __init__(self, city):
        self.serverURL = _couchdb_get_url()
        self.city = city

    def load_tweet_data(self):
        # TODO: MapReduce to get data only from the specified city and specified queries
        db = db_util.cdb(self.serverURL, "twitters")
        return db.getAll()

    def load_suburb_coordinates(self):
        city_key = "{}_suburbs".format(self.city.lower())
        db = db_util.cdb(self.serverURL, "aurin")
        return db.get(city_key)

    def load_analysis(self):
        db = db_util.cdb(self.serverURL, "analysis_results")
        city_key = "{}_analysis_result".format(self.city.lower())
        try:
            return db.get(city_key)
        except:
            return None


class tweetAnalyzer():

    def __init__(self):
        self.structure_file = 'config/result.structure.cfg'
        config.read(self.structure_file )
        self.analysis_result = json.loads(config.get('FIRST-LAYER', 'DICT'))

    def create_suburb_polygons(self, suburb_coordinates):
        polygon_dict = {'suburbs': [], 'polygons': []}
        for feature in suburb_coordinates['features']:
            lat_lon_list = feature['geometry']['coordinates'][0][0]
            polygon = Polygon(lat_lon_list)
            polygon_dict['suburbs'].append(feature['properties']['name'])
            polygon_dict['polygons'].append(polygon)
        return polygon_dict

    def get_city(self, tweet_json):
        city = None
        # places = GeoText(tweet_json['place']['name']) # Drysdale - Clifton Springs doesn't work
        try:
            if tweet_json["place"]["place_type"] == "city":
                city = tweet_json["place"]["name"]
        except:
            pass
        return city

    def add_suburb_to_analysis(self, suburb):
        config.read(self.structure_file)
        self.analysis_result['suburbs'][suburb] = json.loads(config.get('SECOND-LAYER', 'SUBURBS'))

    def extract_topic_from_text(self, tweet_json, suburb):
        # if 'covid' in str(tweet_json).lower():
        try:
            text = tweet_json['text'] + tweet_json['extended_tweet']['full_text']
        except:
            text = tweet_json['text']
        if 'covid' in text.lower():
            # TODO: Should also include extended_tweets etc.
            self.analysis_result['suburbs'][suburb]['covid-19']['count'] += 1
        if 'sports' in text.lower():
            pass

    def extract_topic_from_hashtag(self, tweet_json, suburb):
        hashtags = [dict['text'] for dict in tweet_json["entities"]["hashtags"]]
        hashtags_contain_topic = [hashtag for hashtag in hashtags if 'covid' in hashtag.lower()]
        if len(hashtags_contain_topic) > 0:
            self.analysis_result['suburbs'][suburb]['covid-19']['count'] += 1

    def process_topic(self, tweet_json, suburb):
        self.extract_topic_from_text(tweet_json, suburb)
        self.extract_topic_from_hashtag(tweet_json, suburb)

    def match_suburb(self, tweet_json, polygon_dict):
        if tweet_json['geo'] is not None:
            if tweet_json['geo']['type'] == 'Point':
                coordinates = tweet_json['geo']['coordinates']
                point = Point(coordinates[1], coordinates[0])  # AURIN data coordinates are reversed
                for index, polygon in enumerate(polygon_dict['polygons']):
                    if polygon.contains(point):
                        suburb = polygon_dict['suburbs'][index]
                        # TODO: Find out suburb "null".
                        if suburb not in self.analysis_result['suburbs'].keys():
                            self.add_suburb_to_analysis(suburb)
                        else:
                            self.analysis_result['suburbs'][suburb]['count'] += 1
                        self.process_topic(tweet_json, suburb)

    def count_precise_geo(self, tweet_json):
        global geo_count
        if tweet_json['geo'] is not None:
            if tweet_json['geo']['type'] == 'Point':
                geo_count += 1

    def parse_json(self, all_data, polygon_dict):
        for tweet_json in all_data:
            # city = self.get_city(tweet_json)
            # if city is not None:
            #     self.add_update_city_to_analysis(city)
            self.match_suburb(tweet_json, polygon_dict)
        return self.analysis_result


class analysisResultSaver():

    def __init__(self, city):
        self.serverURL = _couchdb_get_url()
        self.city = city

    def save_analysis(self, analysis_result):
        db = db_util.cdb(self.serverURL, "analysis_results")
        analysis_city_id = "{}_analysis_result".format(self.city.lower())
        db.put(analysis_result, analysis_city_id)


if __name__ == '__main__':
    cities = ["Melbourne", "Sydney", "Brisbane", "Adelaide", "Perth"]
    city = cities[0]
    data_loader = dataLoader(city)
    tweet_analyzer = tweetAnalyzer()
    analysis_result_saver = analysisResultSaver(city)

    city_data = data_loader.load_tweet_data()
    suburb_coordinates = data_loader.load_suburb_coordinates()
    old_analysis = data_loader.load_analysis()

    polygon_dict = tweet_analyzer.create_suburb_polygons(suburb_coordinates)
    analysis_result = tweet_analyzer.parse_json(city_data, polygon_dict)

    analysis_result_saver.save_analysis(analysis_result)

