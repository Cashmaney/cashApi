#!/bin/bash

cd /var/app
export PYTHONPATH=/var/app;$PYTHONPATH

python manage.py migrate --noinput
python manage.py initadmin
python manage.py collectstatic --noinput

python manage.py createsuperuser --username=admin --email=admin@test.com --password=orejas123
python manage.py runserver 0.0.0.0:8080
