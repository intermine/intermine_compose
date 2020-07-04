#!/bin/bash

# # Wait for database
# dockerize -wait tcp://postgres:$PGPORT -timeout 60s
until psql -U ${PGUSER:-postgres} -h ${PGHOST:-postgres} -p ${PGPORT:-5432} -c '\l'; do
  echo >&2 "$(date +%Y%m%dt%H%M%S) Postgres is unavailable - sleeping"
  sleep 1
done
echo >&2 "$(date +%Y%m%dt%H%M%S) Postgres is up - executing command"

gunicorn wsgi:app -p compose.pid -b ${FLASK_HOST:-0.0.0.0}:${FLASK_PORT:-9991} 