#!/bin/sh

python3 manage.py migrate
python3 manage.py collectstatic --no-input

gunicorn app.wsgi:application --bind 0:8000
