import os
import json
from nltk.corpus import twitter_samples
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict, Counter
from configparser import ConfigParser
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from analyzer import db_connecter
from better_profanity import profanity


class tweetAnalyzer():

    def __init__(self, city=None):
        self.city = city
        self.structure_file = '{}/config/result.structure.cfg'.format(os.path.pardir)
        self.config = ConfigParser()
        self.suburb_info_json = db_connecter.dataLoader(self.city).load_city_suburb_coordinates()
        self.city_scenarios = ['covid-19', 'crime']
        self.suburb_scenarios = ['income', 'education', 'migration']
        self.load_city_structure()
        self.load_suburbs_structure()
        self.sentiment_analyser = SentimentIntensityAnalyzer()
        profanity.load_censor_words()

    def load_city_structure(self):
        """
        Load result structure for city level analysis
        """
        self.config.read(self.structure_file)
        self.analysis_result = json.loads(self.config.get('FIRST-LAYER', 'CITY'))
        self.analysis_result['city_name'] = self.city
        for scenario in self.city_scenarios:
            self.analysis_result[scenario] = json.loads(self.config.get('SECOND-LAYER', scenario.upper()))
        self.polygon_dict = None

    def load_suburbs_structure(self):
        """
        Load result structure for suburb level analysis
        :return:
        """
        # suburb_json_file = '{}/suburbs/{}_suburbs.json'.format(os.path.pardir, self.city)
        # with open(suburb_json_file) as f:
        #     suburb_info_json = json.load(f)
        for feature in self.suburb_info_json['features']:
            suburb = feature['properties']['name']
            self.analysis_result['suburbs'][suburb] = json.loads(self.config.get('SECOND-LAYER', 'SUBURB'))
            for scenario in self.suburb_scenarios:
                self.analysis_result['suburbs'][suburb][scenario] = json.loads(self.config.get('THIRD-LAYER', scenario.upper()))

    def create_suburb_polygon_dict(self):
        """
        Create suburb polygon by using coordinates, and save it as a read-easy form.
        :return: dictionary. value of key 'suburbs' is a list of suburb names.
                             value of key 'polygons' is a list of polygons.
        """
        polygon_dict = {'suburbs': [], 'polygons': []}
        # suburb_json_file = '{}/suburbs/{}_suburbs.json'.format(os.path.pardir, self.city)
        # with open(suburb_json_file) as f:
        #     suburb_info_json = json.load(f)
        for feature in self.suburb_info_json['features']:
            lat_lon_list = feature['geometry']['coordinates'][0][0]
            polygon = Polygon(lat_lon_list)
            polygon_dict['suburbs'].append(feature['properties']['name'])
            polygon_dict['polygons'].append(polygon)
        return polygon_dict

    def get_city(self, tweet_json):
        """
        :return: city of the tweet being tweeted.
        """
        city = None
        try:
            if tweet_json["place"]["place_type"] == "city":
                city = tweet_json["place"]["name"]
        except:
            pass
        return city

    def add_suburb_to_analysis(self, suburb):
        """
        Add suburb level structure for given suburb.
        """
        self.analysis_result['suburbs'][suburb] = json.loads(self.config.get('SECOND-LAYER', 'SUBURB'))
        for scenario in self.city_scenarios:
            self.analysis_result['suburbs'][suburb][scenario] = json.loads(self.config.get('THIRD-LAYER', scenario.upper()))

    def judge_attitude(self, text, suburb=None):
        """
        Judge the attitude of the covid-19 related tweet.
        """
        attitude_score = self.sentiment_analyser.polarity_scores(text)['compound']
        attitude = 'tweet_positive_count' if attitude_score > 0.25 else 'tweet_negative_count' \
            if attitude_score < -0.25 else 'tweet_neutral_count'
        if suburb:
            self.analysis_result['suburbs'][suburb]['covid-19'][attitude] += 1
        self.analysis_result['covid-19'][attitude] += 1

    def process_covid_19(self, tweet_json):
        """
        Process COVID-19 scenario analysis on the tweet.
        """
        text = tweet_json['text']
        # TODO: Should also include extended_tweets etc.
        # TODO: Extract from hashtag
        if 'covid' in str(tweet_json).lower() or '新冠' in str(tweet_json).lower():
        # if 'covid' in text.lower():
            self.analysis_result['covid-19']['tweet_count'] += 1
            # self.judge_attitude(text, suburb)
            if tweet_json['lang'] == 'en':
                self.analysis_result['covid-19']['english_count'] += 1
            if tweet_json['lang'] == 'zh-cn' or tweet_json['lang'] == 'zh-tw' or tweet_json['lang'] == 'zh':
                self.analysis_result['covid-19']['chinese_count'] += 1
            if tweet_json['lang'] == 'es':
                self.analysis_result['covid-19']['spanish_count'] += 1
            if tweet_json['lang'] != 'en' and tweet_json['lang'] != 'zh-cn' \
                    and tweet_json['lang'] != 'zh-tw' and tweet_json['lang'] != 'es':
                self.analysis_result['covid-19']['others_count'] += 1

    # def extract_topic_from_hashtag(self, tweet_json, suburb):
    #     hashtags = [dict['text'] for dict in tweet_json["entities"]["hashtags"]]
    #     hashtags_contain_topic = [hashtag for hashtag in hashtags if 'covid' in hashtag.lower()]
    #     if len(hashtags_contain_topic) > 0:
    #         self.analysis_result['suburbs'][suburb]['covid-19']['tweet_count'] += 1

    def process_crime(self, tweet_json):
        """
        Process CRIME scenario analysis on the tweet.
        """
        # TODO: It's better to use full-text instead
        text = tweet_json['text']
        if profanity.contains_profanity(text):
            self.analysis_result['crime']['vulgar_tweet_count'] += 1

    def process_income(self, tweet_json, suburb):
        text = tweet_json['text']
        attitude_score = self.sentiment_analyser.polarity_scores(text)['compound']
        attitude = 'tweet_positive_count' if attitude_score > 0.25 else 'tweet_negative_count' \
            if attitude_score < -0.25 else 'tweet_neutral_count'
        if suburb:
            self.analysis_result['suburbs'][suburb]['income'][attitude] += 1

    def process_education(self, tweet_json, suburb):
        text = tweet_json['text']
        if profanity.contains_profanity(text):
            if suburb:
                self.analysis_result['suburbs'][suburb]['education']['vulgar_tweet_count'] += 1

    def process_migration(self, tweet_json, suburb):
        if tweet_json['lang'] != 'en':
            if suburb:
                self.analysis_result['suburbs'][suburb]['migration']['non_english_tweet_count'] += 1

    def process_scenarios(self, tweet_json, suburb=None):
        """
        Process scenarios for the tweet.
        """
        self.process_covid_19(tweet_json)
        self.process_crime(tweet_json)
        self.process_income(tweet_json, suburb)
        self.process_education(tweet_json, suburb)
        self.process_migration(tweet_json, suburb)

    def match_suburb(self, tweet_json, polygon_dict):
        """
        Find the suburb where the tweet was tweeted.
        :param tweet_json:
        :param polygon_dict:
        :return:
        """
        if self.get_city(tweet_json) == self.city:
            self.analysis_result['city_tweet_count'] += 1
            if tweet_json['geo']:
                if tweet_json['geo']['type'] == 'Point':
                    self.analysis_result['city_tweet_with_geo_count'] += 1
                    coordinates = tweet_json['geo']['coordinates']
                    point = Point(coordinates[1], coordinates[0])  # AURIN data coordinates are reversed
                    for index, polygon in enumerate(polygon_dict['polygons']):
                        if polygon.contains(point):
                            suburb = polygon_dict['suburbs'][index]
                            self.analysis_result['suburbs'][suburb]['suburb_tweet_count'] += 1
                            return suburb
            else:
                return None

    def analyze(self, city_data):
        polygon_dict = self.create_suburb_polygon_dict()
        for tweet_json in city_data:
            suburb = self.match_suburb(tweet_json, polygon_dict)
            self.process_scenarios(tweet_json, suburb)
        return self.analysis_result


def load_timestamp_record():
    with open('timestamp_record.json', 'r') as f:
        record = json.load(f)
        start_ts = record["tweets_with_geo"]
        end_ts = str(int(start_ts) + 100)
    return start_ts, end_ts


def update_timestamp_record():
    with open('timestamp_record.json', 'r') as f:
        record = json.load(f)
        start_ts = record["tweets_with_geo"]
        end_ts = int(start_ts) + 100
    with open('timestamp_record.json', 'w')  as f:
        record["tweets_with_geo"] = end_ts
        json.dump(record, f, indent=1)


if __name__ == '__main__':
    # TODO: Receive city parameter from backend.
    cities = ["Melbourne", "Sydney", "Brisbane", "Adelaide", "Perth (WA)"]
    city = cities[1].split(" ")[0]

    # TODO: Solve extended form. (By other offline functions. Formalize all data.)
    data_loader = db_connecter.dataLoader(city)
    analysis_result_saver = db_connecter.analysisResultSaver(city)
    tweet_analyzer = tweetAnalyzer(city)

    # start_ts, end_ts = load_timestamp_record()
    # city_period_data = data_loader.load_period_tweet_data(start_ts, end_ts)
    # analysis_result = tweet_analyzer.analyze(city_period_data)
    # analysis_result_saver.update_analysis(analysis_result)
    # update_timestamp_record()

    city_data = data_loader.load_tweet_data()
    analysis_result = tweet_analyzer.analyze(city_data)
    analysis_result_saver.save_analysis(analysis_result)
