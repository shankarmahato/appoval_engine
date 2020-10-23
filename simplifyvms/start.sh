#!/bin/sh
python manage.py makemigrations
python manage.py migrate
# python manage.py loaddata fixtures/dataset/*.json
#nohup python manage.py runserver 0.0.0.0:8000 &
python manage.py collectstatic --noinput
gunicorn simplifyvms.wsgi:application --bind 0.0.0.0:8000 
# python manage.py pubsub '/approvals' approval_engine.task.submit_approval


exec "$@"