# Use the official Python 3.12 slim image as the base image
FROM python:3.12.3-slim

# Prevent Python from writing pyc files to disk & enable stdout/stderr logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/

# Copy the entrypoint script and make it executable
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port 8000 for the application
EXPOSE 8000

# Use the entrypoint script to run migrations, collect static files, create superuser, and launch Gunicorn
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command to run Gunicorn
CMD ["gunicorn", "expense_tracker_api.wsgi:application", "--bind", "0.0.0.0:8000"]
