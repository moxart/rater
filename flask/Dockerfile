FROM python:3-slim-buster

LABEL maintainer="Patrick Avakian moxart@moxart.ir"

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt