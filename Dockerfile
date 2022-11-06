# pull official base image
FROM python:3.9-slim-buster

# set working directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql libpq-dev curl \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry export -f requirements.txt --output requirements.txt

RUN pip install -r requirements.txt

# add app
COPY . .
