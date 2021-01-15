FROM python:3.8-slim-buster

ENV VENV=venv
ENV PATH="$VENV/bin:$PATH"

RUN apt-get update -y && \
    apt-get upgrade -y && \
    && apt-get install gcc python3-venv python3-dev -y \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv $VENV
RUN . venv/bin/activate && \
    RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . .

EXPOSE 8000
