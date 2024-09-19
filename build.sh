#!/usr/bin/env bash
# exit on error
set -o errexit

# Ensure python and pip are installed
python3 --version
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip

# Install dependencies
pip3 install -r requirements.txt

# Collect static files for Django
python3 manage.py collectstatic --no-input

# Optionally create superuser if environment variable is set
if [[ $CREATE_SUPERUSER ]]; then
  python3 manage.py createsuperuser --no-input
fi
