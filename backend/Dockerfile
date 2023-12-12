# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install Flask-CORS Flask-JWT-Extended Flask-Bcrypt couchbase rethinkdb looseversion
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]