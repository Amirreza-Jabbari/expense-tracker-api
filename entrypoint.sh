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

# Create a superuser if environment variables are provided and the user does not exist
if [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Creating superuser if not exists..."
  python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User = get_user_model(); admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL'); admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD'); (admin_email and admin_password and not User.objects.filter(email=admin_email).exists()) and User.objects.create_superuser(email=admin_email, password=admin_password)"
fi

# Execute the container's main process (Gunicorn)
exec "$@"
