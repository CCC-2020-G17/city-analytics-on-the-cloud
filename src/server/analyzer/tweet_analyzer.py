import os
import sys
import json
import logging
import tweepy
import time
import datetime
from multiprocessing import Process
from configparser import ConfigParser
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from better_profanity import profanity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from analyzer import db_connecter


process_time_interval = 1000


class tweetAnalyzer():

    def __init__(self, city=None):
        self.city = city
        self.structure_file = '{}/config/result.structure.cfg'.format(os.path.pardir)
        self.config = ConfigParser()
        self.suburb_info_json = db_connecter.dataLoader(self.city).load_city_suburb_coordinates()
        self.city_scenarios = ['covid-19','young_twitter_preference', 'tweet_density']
        self.suburb_scenarios = ['income', 'education', 'migration']
        self.load_city_structure()
        self.load_suburb_structure()
        self.all_user_ids = set()
        self.covid_user_ids = []
        self.sentiment_analyser = SentimentIntensityAnalyzer()
        self.api = tweepy.API(get_twitter_auth(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
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

    def load_suburb_structure(self):
        """
        Load result structure for suburb level analysis
        """
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
        Process city-level COVID-19 scenario analysis on the tweet.
        """
        text = tweet_json['text']
        if 'covid' in str(tweet_json).lower() or 'corona' in str(tweet_json).lower():
            self.analysis_result['covid-19']['tweet_count'] += 1
            if tweet_json['user']['id'] not in  self.covid_user_ids:
                self.covid_user_ids.append(tweet_json['user']['id'])

    def process_crime(self, tweet_json):
        """
        Process city-level CRIME scenario analysis on the tweet.
        """
        text = tweet_json['text']
        if profanity.contains_profanity(text):
            self.analysis_result['crime']['vulgar_tweet_count'] += 1

    def process_night_tweets(self, tweet_json):
        tweet_datetime = tweet_json['created_at']   # This is UTC time
        tweet_time = tweet_datetime.split(' ')[3]
        t0_utc = datetime.datetime.strptime(tweet_time, '%H:%M:%S')
        # Tranform AEST 22:00 - 05:00(+1) to UTC is 12:00 - 19:00
        t1 = t0_utc.replace(hour=12, minute=0, second=0, microsecond=0)
        t2 = t0_utc.replace(hour=19, minute=0, second=0, microsecond=0)
        if t0_utc > t1 and t0_utc < t2:
            self.analysis_result['young_twitter_preference']['night_tweets_count'] += 1

    def process_income(self, tweet_json, suburb):
        """
        Process suburb-level income and tweet sentiment scenario analysis on the tweet
        """
        text = tweet_json['text']
        attitude_score = self.sentiment_analyser.polarity_scores(text)['compound']
        attitude = 'tweet_positive_count' if attitude_score > 0.25 else 'tweet_negative_count' \
            if attitude_score < -0.25 else 'tweet_neutral_count'
        if suburb:
            self.analysis_result['suburbs'][suburb]['income'][attitude] += 1

    def process_education(self, tweet_json, suburb):
        """
        Process suburb-level education and vulgar tweets scenario analysis on the tweet
        """
        text = tweet_json['text']
        if profanity.contains_profanity(text):
            if suburb:
                self.analysis_result['suburbs'][suburb]['education']['vulgar_tweet_count'] += 1

    def process_migration(self, tweet_json, suburb):
        """
        Process suburb-level migration and non-English tweets scenario analysis on the tweet
        """
        if tweet_json['lang'] != 'en':
            if suburb:
                self.analysis_result['suburbs'][suburb]['migration']['non_english_tweet_count'] += 1

    def process_scenarios(self, tweet_json, suburb=None):
        """
        Process scenarios for the tweet.
        """
        self.process_covid_19(tweet_json)
        # self.process_crime(tweet_json)
        self.process_night_tweets(tweet_json)
        self.process_income(tweet_json, suburb)
        self.process_education(tweet_json, suburb)
        self.process_migration(tweet_json, suburb)

    def match_suburb(self, tweet_json, polygon_dict):
        """
        Find the suburb where the tweet was tweeted
        """
        if self.get_city(tweet_json) == self.city:
            self.analysis_result['city_tweet_count'] += 1
            self.all_user_ids.add(tweet_json['user']['id'])
            if tweet_json['geo']:
                if tweet_json['geo']['type'] == 'Point':
                    self.analysis_result['young_twitter_preference']['tweet_with_geo_count'] += 1
                    coordinates = tweet_json['geo']['coordinates']
                    point = Point(coordinates[1], coordinates[0])  # AURIN data coordinates are reversed
                    for index, polygon in enumerate(polygon_dict['polygons']):
                        if polygon.contains(point):
                            suburb = polygon_dict['suburbs'][index]
                            self.analysis_result['suburbs'][suburb]['suburb_tweet_count'] += 1
                            return suburb
            else:
                return None

    def process_covid_followers(self):
        def get_num_followers(user_id):
            influencer = self.api.get_user(user_id=user_id)
            number_of_followers = influencer.followers_count
            return number_of_followers
        followers_within_100 = 0
        followers_100_to_500 = 0
        followers_above_500 = 0
        follower_not_able_to_get = 0
        for user in self.covid_user_ids:
            try:
                num_followers = get_num_followers(user)
                if num_followers < 100:
                    followers_within_100 += 1
                elif num_followers < 500:
                    followers_100_to_500 += 1
                else:
                    followers_above_500 += 1
            except Exception as e:
                print(user, e)
                follower_not_able_to_get += 1
        self.analysis_result['covid-19']['followers_within_100'] = followers_within_100
        self.analysis_result['covid-19']['followers_100_to_500'] = followers_100_to_500
        self.analysis_result['covid-19']['followers_above_500'] = followers_above_500
        self.analysis_result['covid-19']['follower_not_able_to_get'] = follower_not_able_to_get

    def process_avg_tweet_density(self):
        """
        Process Tweets density
        """
        try:
            self.analysis_result['tweet_density']['unique_user_count'] = int(len(self.all_user_ids)/5)
        except:
            self.analysis_result['tweet_density']['unique_user_count'] = len(self.all_user_ids)

    def analyze(self, city_data):
        """
        Process Tweet Analyzing
        """
        polygon_dict = self.create_suburb_polygon_dict()
        for tweet_json in city_data:
            suburb = self.match_suburb(tweet_json, polygon_dict)
            self.process_scenarios(tweet_json, suburb)
        self.process_covid_followers()
        self.process_avg_tweet_density()
        return self.analysis_result


def _setup_analysis_logger():
    """
    Setup a logger for the application
    """
    global logger
    logging.basicConfig(filename='analysis_log.log', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)


def _load_timestamp_record():
    end_time = int(time.time())
    start_time = end_time - process_time_interval
    return start_time, end_time


def get_twitter_auth(section='DEFAULT', verbose=False):
    '''
    Setup Twitter authentication
    :param section: section in twitter key configuration file
    :return: tweepy.OAuthHandler
    '''
    config = ConfigParser()
    key_file = '{}/config/twitter.key.cfg'.format(os.path.pardir)
    if verbose:
        print('key_file {}'.format(key_file))
    config.read(key_file)
    CONSUMER_KEY = config.get(section, 'CONSUMER_KEY')
    CONSUMER_SECRET = config.get(section, 'CONSUMER_SECRET')
    ACCESS_TOKEN = config.get(section, 'ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config.get(section, 'ACCESS_TOKEN_SECRET')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


def analyze_cities():
    start_ts, end_ts = _load_timestamp_record()
    logger.info('The analysis about to make is on data with timestamp from {} to {}'.format(start_ts, end_ts))
    cities = ["Melbourne", "Sydney", "Brisbane", "Adelaide", "Perth (WA)"]
    for city in cities:
        city = city.split(" ")[0]
        data_loader = db_connecter.dataLoader(city)
        analysis_result_saver = db_connecter.analysisResultSaver(city)
        tweet_analyzer = tweetAnalyzer(city)
        city_period_data = data_loader.load_period_tweet_data(start_ts, end_ts)
        analysis_result = tweet_analyzer.analyze(city_period_data)
        analysis_result_saver.update_analysis(analysis_result)


if __name__ == '__main__':
    _setup_analysis_logger()
    while True:
        try:
            process_start_time = time.time()
            analysis_process = Process(target=analyze_cities)
            analysis_process.start()
            analysis_process.join(timeout=100)
            analysis_process.terminate()
            if analysis_process.exitcode is None:
                logger.info('Process timeouts.')
            process_end_time = time.time()
            time_sleep = process_time_interval - (process_end_time - process_start_time)
            logger.info('Sleep for {} seconds...'.format(int(time_sleep)))
            time.sleep(time_sleep)
        except Exception as e:
            logger.exception(e)

    # The code below is for analyzing all data
    # cities = ["Melbourne", "Sydney", "Brisbane", "Adelaide", "Perth"]
    # for city in cities:
    #     data_loader = db_connecter.dataLoader(city)
    #     analysis_result_saver = db_connecter.analysisResultSaver(city)
    #     tweet_analyzer = tweetAnalyzer(city)
    #     city_data = data_loader.load_tweet_data()
    #     analysis_result = tweet_analyzer.analyze(city_data)
    #     analysis_result_saver.save_analysis(analysis_result)


