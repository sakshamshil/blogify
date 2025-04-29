#!/bin/bash
# Make sure we're using the Python from the Vercel environment
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput