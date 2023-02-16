#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py migrate

echo "Starting uwsgi server"
uwsgi --strict --ini uwsgi.ini
