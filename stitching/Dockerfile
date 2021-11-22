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


COPY ./stitching/ashlar /ashlar/
RUN pip3 install /ashlar

ENV OMP_NUM_THREADS 4

## end of ashlar build
WORKDIR /code

RUN pip3 install -q -U \
    celery==4.2.0

## Copy shared  utils
COPY ./utils /code/utils

COPY ./celery_tasks/ /code/celery_tasks/
COPY ./stitching /code

ENTRYPOINT celery -A main worker --concurrency=4 --loglevel=info -n stitching_worker.%h
