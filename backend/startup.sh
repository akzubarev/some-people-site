#!/bin/bash
python manage.py migrate;
python manage.py createcachetable;
python manage.py createsuperuser;
python manage.py loaddata apps/*/fixtures/*.json;
python scripts/load_chars.py;
python manage.py collectstatic;
