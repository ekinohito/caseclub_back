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
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

WORKDIR /usr/src

ENTRYPOINT uvicorn caseclub_back.main:app --reload --host 0.0.0.0 --port 8000