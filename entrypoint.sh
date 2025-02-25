#!/bin/sh

# Wait for PostgreSQL to be available
if [ "$DATABASE_HOST" ]; then
  echo "Waiting for PostgreSQL at $DATABASE_HOST:$DATABASE_PORT..."
  while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
    sleep 0.5
  done
  echo "PostgreSQL is up and running!"
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Execute the container's main process (Gunicorn)
exec "$@"
