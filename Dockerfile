FROM python:3.9-alpine

WORKDIR /app

RUN apk add build-base postgresql-client postgresql-dev libffi-dev libressl-dev openssl-dev

RUN pip install --upgrade pip && pip install pipenv && pip install -U setuptools

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --dev

COPY . /app