#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done
python manage.py migrate

echo "Starting uwsgi server"
uwsgi --strict --ini uwsgi.ini
