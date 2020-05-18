from couchDB.db_util import cdb
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import OAuthHandler
import time
import json
from configparser import ConfigParser


def _couchdb_get_url(section='DEFAULT', verbose=False):
    config = ConfigParser()
    url_file = 'config/server.url.cfg'
    if verbose:
        print('url_file %s' % url_file)
    config.read(url_file)
    server_url = config.get(section, 'server_url')
    return server_url


def _twitter_get_auth(section='DEFAULT', verbose=False):
    # set up twitter authentication
    # Return: tweepy.OAuthHandler object

    config = ConfigParser()
    key_file = 'config/twitter.key.cfg'
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


class MyListener(StreamListener):

    def on_data(self, raw_data):
        server_url = _couchdb_get_url()
        db = cdb(server_url, save_to_db)
        raw_data = json.loads(raw_data)
        try:
            if geo_only:
                if raw_data['geo'] is not None:
                # with open('melb_geo_streaming.json', 'a') as f:
                #     json.dump(raw_data, f, indent=2)
                    db.twput(raw_data)
            else:
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


def get_streaming_twitters():
    auth = _twitter_get_auth(api_access)
    twitter_stream = Stream(auth, MyListener())
    # use filter to collect twitter information based on Australia field
    while True:
        try:
            twitter_stream.filter(locations=[114.46, -38.28, 152.7, -11.79])
        except Exception as e:
            print('Exception:', e)
        pass


if __name__ == '__main__':
    api_access = 'SECTION2'
    save_to_db = 'tweets_mixed'
    geo_only = False
    get_streaming_twitters()



# with open('./tweet_havester_config.json','r') as f:
#     dict = json.load(f)
#     for city in dict:
#         try:
#             get_streaming_twitters(dict[city]["bound"])
#         except Exception as e:
#             print(e)
#         pass
# f.close()

