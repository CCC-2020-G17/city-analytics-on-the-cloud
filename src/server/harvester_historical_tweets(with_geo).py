import tweepy
from tweepy import API
from tweepy import OAuthHandler
from configparser import ConfigParser
from db_util import cdb
import time
import json


def _couchdb_get_url(section='DEFAULT', verbose=False):
    config = ConfigParser()
    url_file = 'config/server.url.cfg'
    if verbose:
        print('url_file %s' % url_file)
    config.read(url_file)
    server_url = config.get(section, 'server_url')
    return server_url


def get_twitter_auth(section='DEFAULT', verbose=False):
    #set up twitter authentication
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


"""TwitterAPI can only search tweets posted in the last 7 days."""
def get_historical_twitters(since_time, until_time):
    auth = get_twitter_auth()
    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    server_url = _couchdb_get_url()
    db = cdb(server_url, 'test')

    places = api.geo_search(query="AU", granularity="country")
    place_id = places[0].id
    tweets = tweepy.Cursor(api.search, q="place:%s" % place_id, since=since_time, until=until_time,
                               tweet_mode='extended').items()
    while True:
        try:
            tweet = tweets.next()
            print(tweet._json)
            if tweet._json['geo'] is not None:
                with open('historical_data.json', 'a') as f:
                    json.dump(tweet._json, f, indent=2)
                    db.twput(tweet._json)
        except tweepy.TweepError:
            print("Rate limit reached. Sleeping for: 60 * 15")
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break


if __name__ == '__main__':
    since_time = '2020-04-22'
    until_time = '2020-04-23'
    get_historical_twitters(since_time, until_time)





