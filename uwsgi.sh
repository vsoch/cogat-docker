#!/bin/bash
python /code/manage.py makemigrations
python /code/manage.py migrate
python /code/manage.py collectstatic --noinput
uwsgi --ini /code/uwsgi.ini
