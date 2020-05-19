FROM python:3

RUN mkdir -p config couchDB

COPY ["tweet_harvester_hist.py", "./"]
COPY couchDB ./couchDB/

RUN pip install tweepy couchdb

CMD python tweet_harvester_hist.py