#!/bin/bash
echo "Waiting for MongoDB connection"
echo "$MONGO_HOST"
echo$ "$MONGO_PORT"

while ! nc -z $MONGO_HOST $MONGO_PORT; do
    sleep 0.1
done

echo "MongoDB started"

exec "$@"