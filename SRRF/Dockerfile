FROM ubuntu:18.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        build-essential \
        ffmpeg \
        git \
        libfftw3-dev \
        libfftw3-double3 \
        libfftw3-long3 \
        libfftw3-single3 \
        openjdk-11-jdk-headless \
        python3-dev \
        python3-pip \
        python3-tk \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -q -U \
    cython \
    numpy \
    pip

ENV OMP_NUM_THREADS 4

## start of SRRF worker build
WORKDIR /app

COPY ./SRRF/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

## Copy shared utils
COPY ./shared_utils /app/shared_utils/

COPY ./celery_tasks/ /app/celery_tasks/
COPY ./SRRF /app

#ENTRYPOINT celery -A SRRF.main worker --concurrency=4 --loglevel=info -n stitching_worker.%h
#ENTRYPOINT python3 ./SRRF/main.py
