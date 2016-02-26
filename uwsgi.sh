#!/bin/bash
while ! nc -z graphdb 7474; do sleep 3; done

python /app/manage.py makemigrations
python /app/manage.py migrate
python /app/manage.py collectstatic --noinput
uwsgi --ini /app/uwsgi.ini
