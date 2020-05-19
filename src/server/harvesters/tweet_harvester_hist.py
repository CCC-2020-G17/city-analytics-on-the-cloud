import tweepy
from tweepy import API
from tweepy import OAuthHandler
from configparser import ConfigParser
from couchDB.db_util import cdb
import datetime
import time
import json
import os
import sys


def _couchdb_get_url(section='DEFAULT', verbose=False):
    global config
    config = ConfigParser()
    url_file = '{}/config/server.url.cfg'.format(os.path.pardir)
    if verbose:
        print('url_file {}'.format(url_file))
    config.read(url_file)
    server_url = config.get(section, 'server_url')
    return server_url


def _get_twitter_auth(section='DEFAULT', verbose=False):
    #set up twitter authentication
    # Return: tweepy.OAuthHandler object

    config = ConfigParser()
    key_file = '{}/config/twitter.key.cfg'.format(os.path.pardir)
    if verbose:
        print('key_file %s' % key_file)
    config.read(key_file)
    print(config.keys())
    CONSUMER_KEY = config.get(section, 'CONSUMER_KEY')
    CONSUMER_SECRET = config.get(section, 'CONSUMER_SECRET')
    ACCESS_TOKEN = config.get(section, 'ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config.get(section, 'ACCESS_TOKEN_SECRET')

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


def _get_place_id(city):
    city_bound_file = '{}/config/city_bound.json'.format(os.path.pardir)
    with open(city_bound_file,'r') as f:
        city_bound = json.load(f)
        try:
            place_id = city_bound[city]["place_id"]
        except Exception as e:
            print(e)
        pass
    return place_id


"""TwitterAPI can only search tweets posted in the last 7 days."""
def get_historical_twitters(place_id, since_time, until_time):
    auth = _get_twitter_auth(api_access)
    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    server_url = _couchdb_get_url()
    db = cdb(server_url, save_to_db)

    # places = api.geo_search(query="AU", granularity="country")
    # place_id = places[0].id
    tweets = tweepy.Cursor(api.search, q="place:%s" % place_id, since=since_time, until=until_time).items()
    while True:
        try:
            tweet = tweets.next()
            if geo_only:
                if tweet._json['geo'] is not None:
                    # print(tweet._json)
                    db.twput(tweet._json)
            else:
                # with open('hist.json', 'a') as f:
                #     json.dump(tweet._json, f, indent=2)
                db.twput(tweet._json)
        except tweepy.TweepError:
            print("Rate limit reached. Sleeping for: 60 * 15")
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break


if __name__ == '__main__':
    api_access = 'DEFAULT'
    save_to_db = 'tweets_mixed'
    geo_only = False
    place_id = '3f14ce28dc7c4566'
    until_time = datetime.datetime.now()
    until_time_format = until_time.strftime('%Y-%m-%d')
    since_time = until_time + datetime.timedelta(days=-7)
    since_time_format = since_time.strftime('%Y-%m-%d')
    # print(since_time_format)
    # print(until_time_format)
    """
    USAGE:      python .py <options>
    EXAMPLES:   (1) python tweet_harvester_hist.py
                    - harvest tweets in the whole Australia for the last seven days
                (2) python tweet_harvester_hist.py 2020-05-19 2020-05-20
                    - harvest tweets in the whole Australia for the certain time
                (3) python tweet_harvester_hist.py Melbourne 2020-05-19 2020-05-20
                    - harvest tweets in the Melbourne for the certain day by default api
                (4) python tweet_harvester_hist.py Melbourne 2020-05-19 2020-05-20 SECTION1
                    - harvest tweets in the Melbourne by 'SECTION1' api
    NOTE:       The first argument should be "Adelaide", "Brisbane", "Melbourne", "Perth" or "Sydney".
                The second argument is the since_time: "2020-05-14"
                The third argument is the until_time: "2020-05-17"
                The fourth argument should be "SECTION1", "SECTION2", "SECTION3", "SECTION4" or "SECTION5".
    """

    try:
        if len(sys.argv) == 1:
            get_historical_twitters(place_id, since_time_format, until_time_format)
        elif len(sys.argv) == 3:
            since_time_format = sys.argv[1]
            until_time_format = sys.argv[2]
            get_historical_twitters(place_id, since_time_format, until_time_format)
        elif len(sys.argv) == 4:
            city = sys.argv[1]
            since_time_format = sys.argv[2]
            until_time_format = sys.argv[3]
            place_id = _get_place_id(city)
            get_historical_twitters(place_id, since_time_format, until_time_format)
        else:
            city = sys.argv[1]
            since_time_format = sys.argv[2]
            until_time_format = sys.argv[3]
            api_access = sys.argv[4]
            place_id = _get_place_id(city)
            get_historical_twitters(place_id, since_time_format, until_time_format)
    except Exception as e:
        print(e)
        print("Please check your command! ")







