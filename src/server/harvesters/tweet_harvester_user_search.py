import tweepy
from tweepy import OAuthHandler
from configparser import ConfigParser
from couchDB.db_util import cdb
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


def write_to_db(db, tweet):
    db.twput(tweet)


def get_all_tweets(api, db, userId, startId):
    # initialize a list to hold all the Tweets
    alltweets = []
    # make initial request for most recent tweets
    # (200 is the maximum allowed count)
    new_tweets = api.user_timeline(id=userId, since_id=startId, count=200)
    # save most recent tweets
    if len(new_tweets) > 0:
        alltweets.extend(new_tweets)
        # save the id of the oldest tweet less one to avoid duplication
        endId = alltweets[0].id
        oldest = alltweets[-1].id - 1
        # keep grabbing tweets until there are no tweets left
        while len(new_tweets) > 0:
            # print("getting tweets before %s" % (oldest))
            # all subsequent requests use the max_id param to prevent
            # duplicates
            new_tweets = api.user_timeline(id=userId, since_id=startId, max_id=oldest, count=200)
            # save most recent tweets
            alltweets.extend(new_tweets)
            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            print("...%s tweets downloaded so far" % (len(alltweets)))
        for tweet in alltweets:
            # with open('alltweets.json', 'a') as f:
            #     json.dump(tweet._json, f, indent=2)
            write_to_db(db, tweet._json)
            # print(tweet._json)
        return userId, endId
    else:
        return userId, startId


def get_twitters_by_userIDs():
    server_url = _couchdb_get_url()
    db = cdb(server_url, save_to_db)

    auth = get_twitter_auth()
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # grab tweets by each userID
    with open("userId_search_record.json", 'r') as f:
        for line in f:
            userId_search_record = json.loads(line)
            new_userId_search_record = {}
            for user_id, startId in userId_search_record.items():
                userId, endId = get_all_tweets(api, db, user_id, startId)
                new_userId_search_record[userId] = endId
                with open("userId_search_record2.json", 'a') as f:
                    json.dump(new_userId_search_record, f)
                    f.write("\n")


if __name__ == '__main__':
    save_to_db = 'tweets_mixed'
    get_twitters_by_userIDs()
