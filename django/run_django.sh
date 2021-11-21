#!/bin/sh

# wait for database to start
sleep 3

cd /code/api

su -c "python manage.py collectstatic -y"
#su -c "python manage.py makemigrations"
# migrate db, so we have the latest db schema
#su -c "python manage.py migrate"
# start development server on public ip interface, on port 8000
#su -m myuser -c "python manage.py runserver 0.0.0.0:8000"

# start development server on public ip interface, on port 8000
su -c "gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --timeout 36000"