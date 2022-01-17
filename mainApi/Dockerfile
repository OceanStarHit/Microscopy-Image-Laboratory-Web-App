FROM python:3.8-slim
# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# additional dependencies
# netcat used for checking for resources on the network before start, see start.sh for use
RUN apt-get update && \
    apt-get install -y netcat 
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

COPY ./mainApi/requirements.txt /app/requirements.txt

RUN pip install --upgrade -r /app/requirements.txt

EXPOSE 8000

COPY ./mainApi /app/mainApi/

RUN chmod -R 777 /app/mainApi/app/static

## Copy shared
COPY ./shared_utils /app/shared_utils/
COPY ./celery_tasks/ /app/celery_tasks/


