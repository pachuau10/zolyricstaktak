#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Collect static files for WhiteNoise
python manage.py collectstatic --no-input

# 3. Apply database migrations to Neon
python manage.py migrate

# 4. Create the cache table (required by your settings)
python manage.py createcachetable