#!/bin/sh

# wait for database to start
sleep 3

#python manage.py collectstatic --noinput
#python manage.py makemigrations --noinput
# migrate db, so we have the latest db schema
echo "Collecting Static Files"
su -c "python manage.py collectstatic --noinput"

#echo "Making migrations"
#su -c "python manage.py makemigrations --noinput"

#echo "Migrating"
#su -c "python manage.py migrate --noinput"
#su -c "python manage.py migrate --noinput"
# start development server on public ip interface, on port 8000
#su -m myuser -c "python manage.py runserver 0.0.0.0:8000"


# start development server on public ip interface, on port 8000
echo "Starting Gunicorn and serving Django"
su -c "gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --timeout 36000"