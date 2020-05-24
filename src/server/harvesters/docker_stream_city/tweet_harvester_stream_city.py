from couchDB.db_util import cdb
from tweepy import Stream
from tweepy.streaming import StreamListener
from configparser import ConfigParser
from tweepy import OAuthHandler
import time
import json
import os
import sys


def _couchdb_get_url(section='DEFAULT', verbose=False):
    config = ConfigParser()
    url_file = '{}/config/server.url.cfg'.format(os.path.pardir)
    if verbose:
        print('url_file %s' % url_file)
    config.read(url_file)
    server_url = config.get(section, 'server_url')
    return server_url


def _twitter_get_auth(section='DEFAULT', verbose=False):
    # set up twitter authentication
    # Return: tweepy.OAuthHandler object

    config = ConfigParser()
    key_file = '{}/config/twitter.key.cfg'.format(os.path.pardir)
    if verbose:
        print('key_file %s' % key_file)
    config.read(key_file)
    CONSUMER_KEY = config.get(section, 'CONSUMER_KEY')
    CONSUMER_SECRET = config.get(section, 'CONSUMER_SECRET')
    ACCESS_TOKEN = config.get(section, 'ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config.get(section, 'ACCESS_TOKEN_SECRET')

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


def _get_city_bound(city):
    locations = None
    city_bound_file = '{}/config/city_bound.json'.format(os.path.pardir)
    with open(city_bound_file,'r') as f:
        city_bound = json.load(f)
        try:
            locations = city_bound[city]["bound"]
        except Exception as e:
            print(e)
        pass
    return locations


class MyListener(StreamListener):

    def on_data(self, raw_data):
        server_url = _couchdb_get_url()
        db = cdb(server_url, save_to_db)
        raw_data = json.loads(raw_data)
        try:
            if geo_only:
                if raw_data['geo'] is not None:
                    db.twput(raw_data)
            else:
                # with open('streaming.json', 'a') as f:
                #     json.dump(raw_data, f, indent=2)
                db.twput(raw_data)
            return True

        except BaseException as e:
            print("Error on_data:%s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            print("ERROR: Rate limit reached")
        print(status_code)
        return True

    def on_timeout(self):
        print("ERROR: Timeout...")
        return True  # Don't kill the stream


def get_streaming_twitters(locations=[114.46, -38.28, 152.7, -11.79]):
    auth = _twitter_get_auth(api_access)
    twitter_stream = Stream(auth, MyListener())
    # use filter to collect twitter information based on Australia field
    print("Start getting real time tweets ...")
    while True:
        try:
            twitter_stream.filter(locations=locations)
        except Exception as e:
            print('Exception:', e)
        pass


if __name__ == '__main__':
    api_access = 'DEFAULT'
    save_to_db = 'tweets_mixed'
    geo_only = False

    """
    USAGE:      python .py <options>
    EXAMPLES:   (1) python tweet_harvester_stream.py
                    - harvest real time tweets in the whole Australia
                (2) python tweet_harvester_stream.py Melbourne
                    - harvest real time tweets in the Melbourne by default api
                (3) python tweet_harvester_stream.py Melbourne SECTION1 
                    - harvest real time tweets in the Melbourne by 'SECTION1' api
    NOTE:       The first argument should be "Adelaide", "Brisbane", "Melbourne", "Perth" or "Sydney".
                The second argument should be "SECTION1", "SECTION2", "SECTION3"， "SECTION4" or "SECTION5".    
    """
    
    try:
        if len(sys.argv) == 1:
            print("Collecting twitters for all")
            get_streaming_twitters()
        elif len(sys.argv) == 2:
            city = sys.argv[1]
            location = _get_city_bound(city)
            print("Collecting tweets for ", city)
            get_streaming_twitters(locations=location)
        else:
            city = sys.argv[1]
            api_access = sys.argv[2]
            location = _get_city_bound(city)
            print("Collecting tweets for ", city)
            get_streaming_twitters(locations=location)
    except Exception as e:
        print(e)
        print("Please check your command! ")



