#!/bin/sh
sleep 3
python3 manage.py makemigrations
python3 manage.py migrate
python manage.py collectstatic
gunicorn --bind 0.0.0.0:8000 --workers 3 rockitchef_project.wsgi:application
