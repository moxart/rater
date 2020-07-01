FROM python:3.8.2

LABEL maintainer="Patrick Avakian moxart@moxart.ir"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/flask

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt 

COPY . .