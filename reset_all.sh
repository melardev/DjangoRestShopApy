#!/usr/bin/env bash

# taken from https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

rm db.sqlite3

python3 manage.py makemigrations
python3 manage.py migrate
python3 seed_db.py