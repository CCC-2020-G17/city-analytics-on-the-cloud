FROM python:3

ENV CITY Sydney
ENV TOKEN SECTION2

RUN mkdir -p config couchDB

COPY ["tweet_harvester_hist_city.py", "./"]
COPY couchDB ./couchDB/

RUN pip install tweepy couchdb

CMD python tweet_harvester_hist_city.py $CITY $TOKEN