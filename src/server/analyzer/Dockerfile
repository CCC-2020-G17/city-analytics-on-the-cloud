FROM python:3

RUN mkdir -p config analyzer couchDB

COPY requirements.txt /
COPY couchDB ./couchDB/
COPY __init__.py /analyzer
COPY db_connecter.py /analyzer
COPY tweet_analyzer.py /
#COPY timestamp_record.json /analyzer

RUN pip install -r requirements.txt

CMD python tweet_analyzer.py