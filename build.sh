#!/usr/bin/env bash

# Optional: Export env vars if needed
export DATABASE_URL=$DATABASE_URL
export SECRET_KEY=$SECRET_KEY
export DJANGO_SETTINGS_MODULE=quatra_coffee.settings

pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
