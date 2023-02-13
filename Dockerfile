FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY stripe_project /stripe_project
WORKDIR /stripe_project
EXPOSE 8000

RUN apk add build-base

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user

