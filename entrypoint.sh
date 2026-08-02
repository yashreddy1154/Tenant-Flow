#!/bin/bash

# Exit on error
set -e

echo "Waiting for PostgreSQL to be ready..."
# A simple wait loop using python (since we don't have netcat)
python -c "
import socket, time
host = 'db'
port = 5432
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        break
    except socket.error:
        time.sleep(1)
"
echo "PostgreSQL is ready!"

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"
