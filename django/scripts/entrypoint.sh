#!/bin/sh

if [ "$DATABASE" = "mariadb" ]
then
    echo "Waiting for MariaDB..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "MariaDB started"
fi

# python3 manage.py flush --no-input
# python3 manage.py migrate

exec "$@"