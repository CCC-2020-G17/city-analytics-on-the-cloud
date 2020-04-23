import json
import db_util
from collections import defaultdict, Counter
# from geotext import GeoText


def load_tweet_data():
    serverURL = "http://admin:admin1234@172.26.130.149:5984/"
    db = db_util.cdb(serverURL, "twitters")
    return db.getAll()


def load_analysis():
    serverURL = "http://admin:admin1234@172.26.130.149:5984/"
    db = db_util.cdb(serverURL, "analysis")
    return db.getAll()


def get_city(tweet_json):
    city = None
    # places = GeoText(tweet_json['place']['name']) # Drysdale - Clifton Springs doesn't work
    try:
        city = tweet_json['place']['full_name'].split(",")[0]
    except:
        pass
    return city


def add_update_city(city):
    if city not in analysing_result.keys():
        analysing_result[city] = {
            'total_count': 0,
            'COVID-19': {
                'count': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0
            },
            'sports': {

            }
        }
    analysing_result[city]['total_count'] += 1


def extract_topic_from_text(city, tweet_json):
    # if 'covid' in str(tweet_json).lower():
    try:
        text = tweet_json['text'] + tweet_json['extended_tweet']['full_text']
    except:
        text = tweet_json['text']
    if 'covid' in text.lower():
        # TODO: Should also include extended_tweets etc.
        analysing_result[city]['COVID-19']['count'] += 1
    if 'sports' in text.lower():
        pass


def extract_topic_from_hashtag(city, tweet_json):
    hashtags = [dict['text'] for dict in tweet_json["entities"]["hashtags"]]
    hashtags_contain_topic = [hashtag for hashtag in hashtags if 'covid' in hashtag.lower()]
    if len(hashtags_contain_topic) > 0:
        analysing_result[city]['COVID-19']['count'] += 1


def process_topic(city, tweet_json):
    extract_topic_from_text(city, tweet_json)
    extract_topic_from_hashtag(city, tweet_json)


def count_precise_geo(tweet_json):
    global geo_count
    if tweet_json['geo'] is not None:
        if tweet_json['geo']['type'] == 'Point':
            geo_count += 1


def parse_json_from_file(json_filename):
    with open(json_filename, 'r') as input_file:
        for index, line in enumerate(input_file):
            tweet_json = json.loads(line)
            city = get_city(tweet_json)
            if city is not None:
                add_update_city(city)
                process_topic(city, tweet_json)
                # count_precise_geo(tweet_json)


def parse_json(all_data):
    for json_object in all_data:
        city = get_city(json_object)
        if city is not None:
            add_update_city(city)
            process_topic(city, json_object)


def save_analysis(analysing_result, analysis_id):
    serverURL = "http://admin:admin1234@172.26.130.149:5984/"
    db = db_util.cdb(serverURL, "analysis")
    db.put(analysing_result, analysis_id)


def main():
    global analysing_result
    # global geo_count
    # geo_count = 0
    analysing_result = {}
    all_data = load_tweet_data()
    old_analysis = load_analysis()
    if old_analysis is not None:
        analysis_id = old_analysis[0]['_id']
    else:
        analysis_id = None
    # json_filename = 'tinyData.json'
    parse_json(all_data)
    save_analysis(analysing_result, analysis_id)


if __name__ == '__main__':
    main()