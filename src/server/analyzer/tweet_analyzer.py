import os
import json
from nltk.corpus import twitter_samples
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict, Counter
from configparser import ConfigParser
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from couchDB import db_util
from analyzer import db_connecter
from profanityfilter import ProfanityFilter


class tweetAnalyzer():

    def __init__(self, city=None):
        self.structure_file = '{}/config/result.structure.cfg'.format(os.path.pardir)
        self.config = ConfigParser()
        self.config.read(self.structure_file)
        self.analysis_result = json.loads(self.config.get('FIRST-LAYER', 'CITY'))
        self.polygon_dict = None
        self.city = city

    def create_suburb_polygon_dict(self, suburb_coordinates):
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
        self.config.read(self.structure_file)
        self.analysis_result['suburbs'][suburb] = json.loads(self.config.get('SECOND-LAYER', 'SUBURB'))
        self.analysis_result['suburbs'][suburb]['covid-19'] = json.loads(self.config.get('THIRD-LAYER', 'COVID-19'))
        self.analysis_result['suburbs'][suburb]['crime'] = json.loads(self.config.get('THIRD-LAYER', 'CRIME'))

    def judge_attitude(self, text, suburb=None):
        analyser = SentimentIntensityAnalyzer()
        attitude_score = analyser.polarity_scores(text)['compound']
        if attitude_score > 0.25:
            if suburb:
                self.analysis_result['suburbs'][suburb]['covid-19']['positive'] += 1
            self.analysis_result['covid-19']['positive'] += 1
        elif attitude_score < -0.25:
            if suburb:
                self.analysis_result['suburbs'][suburb]['covid-19']['negative'] += 1
            self.analysis_result['covid-19']['negative'] += 1
        else:
            if suburb:
                self.analysis_result['suburbs'][suburb]['covid-19']['neutral'] += 1
            self.analysis_result['covid-19']['neutral'] += 1

        # attitude = Counter(analyser.polarity_scores(text)).most_common(1)[0][0]
        # if attitude == 'pos':
        #     if suburb:
        #         self.analysis_result['suburbs'][suburb]['covid-19']['positive'] += 1
        #     self.analysis_result['covid-19']['positive'] += 1
        # elif attitude == 'neg':
        #     if suburb:
        #         self.analysis_result['suburbs'][suburb]['covid-19']['negative'] += 1
        #     self.analysis_result['covid-19']['negative'] += 1
        # else:
        #     if suburb:
        #         self.analysis_result['suburbs'][suburb]['covid-19']['neutral'] += 1
        #     self.analysis_result['covid-19']['neutral'] += 1

    def extract_topic_from_text(self, tweet_json, suburb):
        text = tweet_json['text']
        # TODO: Should also include extended_tweets etc.
        if 'covid' in str(tweet_json).lower():
        # if 'covid' in text.lower():
            if suburb is not None:
                self.analysis_result['suburbs'][suburb]['covid-19']['count'] += 1
            self.analysis_result['covid-19']['count'] += 1
            self.judge_attitude(text, suburb)
        if ProfanityFilter().is_profane(text):
            if suburb is not None:
                self.analysis_result['suburbs'][suburb]['crime']['contains_vulgar_count'] += 1
            self.analysis_result['crime']['contains_vulgar_count'] += 1

    def extract_topic_from_hashtag(self, tweet_json, suburb):
        hashtags = [dict['text'] for dict in tweet_json["entities"]["hashtags"]]
        hashtags_contain_topic = [hashtag for hashtag in hashtags if 'covid' in hashtag.lower()]
        if len(hashtags_contain_topic) > 0:
            self.analysis_result['suburbs'][suburb]['covid-19']['count'] += 1

    def process_topic(self, tweet_json, suburb=None):
        self.extract_topic_from_text(tweet_json, suburb)
        # self.extract_topic_from_hashtag(tweet_json, suburb)

    def match_suburb(self, tweet_json, polygon_dict):
        if self.get_city(tweet_json) == self.city:
            self.analysis_result['city_count'] += 1
            if tweet_json['geo']:
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
                                self.analysis_result['suburbs'][suburb]['suburb_count'] += 1
                            self.process_topic(tweet_json, suburb)
            else:
                self.process_topic(tweet_json)

    def count_precise_geo(self, tweet_json):
        global geo_count
        if tweet_json['geo'] is not None:
            if tweet_json['geo']['type'] == 'Point':
                geo_count += 1

    def analyze(self, all_data, polygon_dict):
        for tweet_json in all_data:
            self.match_suburb(tweet_json, polygon_dict)
        return self.analysis_result


if __name__ == '__main__':
    # TODO: Receive city parameter from back end. Load (MapRedude) according to city, Save according to city.
    cities = ["Melbourne", "Sydney", "Brisbane", "Adelaide", "Perth (WA)"]
    city = cities[0].split(" ")[0]

    # TODO: Solve extended form. (By other offline functions. Formalize all data.)
    data_loader = db_connecter.dataLoader(city)
    analysis_result_saver = db_connecter.analysisResultSaver(city)
    tweet_analyzer = tweetAnalyzer(city)

    city_data = data_loader.load_tweet_data()
    suburb_coordinates = data_loader.load_city_suburb_coordinates()
    old_analysis = data_loader.load_analysis()

    polygon_dict = tweet_analyzer.create_suburb_polygon_dict(suburb_coordinates)
    analysis_result = tweet_analyzer.analyze(city_data, polygon_dict)

    analysis_result_saver.save_analysis(analysis_result)

