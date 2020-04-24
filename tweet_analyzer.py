import db_util
from collections import defaultdict, Counter
# from geotext import GeoText
from configparser import ConfigParser
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def _couchdb_get_connection(section='DEFAULT', verbose=False):
    config = ConfigParser()
    url_file = 'server.url.cfg'
    if verbose:
        print('url_file %s' % url_file)
    config.read(url_file)
    server_url = config.get(section, 'server_url')
    return server_url


class dataLoader():

    def __init__(self):
        self.serverURL = _couchdb_get_connection()

    def load_tweet_data(self):
        db = db_util.cdb(self.serverURL, "twitters")
        return db.getAll()

    def load_suburb_coordinates(self, city_key=None):
        if city_key is None:
            city_key = 'f07df51500193e9947a3a84d1e016048'
        db = db_util.cdb(self.serverURL, "aurin")
        return db.get(city_key)

    def load_analysis(self):
        db = db_util.cdb(self.serverURL, "analysis_results")
        return db.getAll()


class tweetAnalyzer():

    def __init__(self):
        self.analysis_result = defaultdict(int)

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
            city = tweet_json['place']['full_name'].split(",")[0]
        except:
            pass
        return city

    def add_update_city_to_analysis(self, city):
        if city not in self.analysis_result.keys():
            self.analysis_result[city] = {
                'total_count': 0,
                'COVID-19': {
                    'count': 0,
                    'positive': 0,
                    'negative': 0,
                    'neutral': 0
                },
                'suburb': {

                }
            }
        self.analysis_result[city]['total_count'] += 1

    def extract_topic_from_text(self, city, tweet_json):
        # if 'covid' in str(tweet_json).lower():
        try:
            text = tweet_json['text'] + tweet_json['extended_tweet']['full_text']
        except:
            text = tweet_json['text']
        if 'covid' in text.lower():
            # TODO: Should also include extended_tweets etc.
            self.analysis_result[city]['COVID-19']['count'] += 1
        if 'sports' in text.lower():
            pass

    def extract_topic_from_hashtag(self, city, tweet_json):
        hashtags = [dict['text'] for dict in tweet_json["entities"]["hashtags"]]
        hashtags_contain_topic = [hashtag for hashtag in hashtags if 'covid' in hashtag.lower()]
        if len(hashtags_contain_topic) > 0:
            self.analysis_result[city]['COVID-19']['count'] += 1

    def process_topic(self, city, tweet_json):
        self.extract_topic_from_text(city, tweet_json)
        self.extract_topic_from_hashtag(city, tweet_json)

    def match_suburb(self, city, tweet_json, polygon_dict):
        if tweet_json['geo'] is not None:
            if tweet_json['geo']['type'] == 'Point':
                coordinates = tweet_json['geo']['coordinates']
                point = Point(coordinates[1], coordinates[0])  # AURIN coordinates are reversed
                for index, polygon in enumerate(polygon_dict['polygons']):
                    if polygon.contains(point):
                        try:
                            self.analysis_result[city]['suburb'][polygon_dict['suburbs'][index]] += 1
                        except:
                            self.analysis_result[city]['suburb'][polygon_dict['suburbs'][index]] = 1

    def count_precise_geo(self, tweet_json):
        global geo_count
        if tweet_json['geo'] is not None:
            if tweet_json['geo']['type'] == 'Point':
                geo_count += 1

    def parse_json(self, all_data, polygon_dict):
        for tweet_json in all_data:
            city = self.get_city(tweet_json)
            if city is not None:
                self.add_update_city_to_analysis(city)
                self.process_topic(city, tweet_json)
                self.match_suburb(city, tweet_json, polygon_dict)
        return self.analysis_result


class analysisResultSaver():

    def __init__(self):
        self.serverURL = _couchdb_get_connection()

    def save_analysis(self, analysis_result, analysis_id):
        db = db_util.cdb(self.serverURL, "analysis_results")
        db.put(analysis_result, analysis_id)


if __name__ == '__main__':
    data_loader = dataLoader()
    tweet_analyzer = tweetAnalyzer()
    analysis_result_saver = analysisResultSaver()

    all_data = data_loader.load_tweet_data()
    old_analysis = data_loader.load_analysis()
    if old_analysis is not None:
        analysis_id = old_analysis[0]['_id']
    else:
        analysis_id = None
    city_key = None
    suburb_coordinates = data_loader.load_suburb_coordinates(city_key)

    polygon_dict = tweet_analyzer.create_suburb_polygons(suburb_coordinates)
    analysis_result = tweet_analyzer.parse_json(all_data, polygon_dict)

    analysis_result_saver.save_analysis(analysis_result, analysis_id)

