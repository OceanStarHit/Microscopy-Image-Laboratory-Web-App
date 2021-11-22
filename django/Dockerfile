FROM python:3.8

#FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y \
    build-essential \
    default-jdk \
    python3.8-dev \
    gcc

RUN python3 -m pip install --upgrade pip

USER root

WORKDIR /code

COPY ./django/requirements.txt .

RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install python-javabridge
RUN python3 -m pip install python-bioformats

#python-javabridge==4.0.3
#python-bioformats==4.0.5

## copy in django
COPY ./django /code

EXPOSE 8000

## Copy shared  utils
COPY ./utils /code/utils

## Copy in celery_tasks so that we can import them in Django
COPY ./celery_tasks /code/celery_tasks/


#RUN chmod +x ./scripts/entrypoin.sh
#RUN sed -i -e 's/\r$//' ./scripts/entrypoint.sh
#RUN ./scripts/entrypoint.sh

