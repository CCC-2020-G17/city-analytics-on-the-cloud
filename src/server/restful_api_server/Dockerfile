FROM python:3

WORKDIR /app

# Improve the build speed
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["uwsgi", "app.ini"]