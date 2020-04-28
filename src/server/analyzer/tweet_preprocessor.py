import re
import string

def remove_hashtags(tweet):
    pass

def remove_mentions(tweet):
    pass

def remove_punctuations(tweet):
    pass

def remove_urls(tweet):
    pass

def clean(tweet):
    tweet = remove_hashtags(tweet)
    tweet = remove_mentions(tweet)
    tweet = remove_urls(tweet)
    tweet = remove_punctuations(tweet)
    return tweet.lower()