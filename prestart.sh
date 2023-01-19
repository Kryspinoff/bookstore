#!/usr/bin/env bash

echo "Waiting for database to be ready"
python3 app/pre_start.py "${@}"

echo "Running migrations"
alembic upgrade head

echo "Initializing defaults data"
python3 app/initial_data.py "${@}"
