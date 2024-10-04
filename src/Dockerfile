FROM python:3.10.13-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/app/backend"

RUN apt update

WORKDIR usr/src/app

RUN mkdir -p $WORKDIR/static
RUN mkdir -p $WORKDIR/media

COPY ./requirements.txt .

RUN pip install --no-cache-dir --no-warn-script-location --upgrade pip && \
    pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt

COPY . .

