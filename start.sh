#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
pip install gunicorn whitenoise

exec gunicorn shinesolar.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
