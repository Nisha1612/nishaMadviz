#!/usr/bin/env bash
# exit on error
set -o errexit

# Ensure pip is installed and Python version is correct
python3.10 -m venv venv
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Collect static files for Django
python manage.py collectstatic --no-input

# Optionally create superuser if the environment variable is set
if [[ $CREATE_SUPERUSER ]]; then
  python manage.py createsuperuser --no-input
fi
