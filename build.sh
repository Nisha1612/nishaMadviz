#!/bin/bash
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
python -m spacy download en_core_web_sm
