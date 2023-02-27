#!/bin/bash

echo "Apply database migrations"
while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done
python manage.py migrate

echo "Compile translation messages"
python manage.py compilemessages

echo "Starting dev server"
python manage.py runserver 0.0.0.0:8000