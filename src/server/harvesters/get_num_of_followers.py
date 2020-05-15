import tweepy
from tweepy import OAuthHandler
from configparser import ConfigParser


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


def get_follower(user_id):
    auth = get_twitter_auth()
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    influencer = api.get_user(user_id=user_id)
    influencer_id = influencer.id
    number_of_followers = influencer.followers_count
    print('user id:', influencer_id, ' | number of followers count:', number_of_followers)


if __name__== '__main__' :
    get_follower("487847291")
    get_follower("489340228")