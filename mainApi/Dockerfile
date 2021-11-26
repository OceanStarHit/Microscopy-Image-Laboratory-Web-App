FROM python:3.8
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./mainApi/requirements.txt /app/requirements.txt

RUN pip install --upgrade -r /app/requirements.txt

EXPOSE 8000

COPY ./mainApi /app/mainApi/

## Copy shared
COPY ./utils /app/utils/
COPY ./celery_tasks/ /app/celery_tasks/

