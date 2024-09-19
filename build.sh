#!/usr/bin/env bash
# exit on error
set -o errexit

# Install python and pip if they aren't available
apt-get update && apt-get install -y python3 python3-pip

# Ensure python and pip are available
python3 --version
pip3 --version

# Install dependencies
pip3 install -r requirements.txt

# Collect static files for Django
python3 manage.py collectstatic --no-input

# Optionally create superuser if environment variable is set
if [[ $CREATE_SUPERUSER ]]; then
  python3 manage.py createsuperuser --no-input
fi
