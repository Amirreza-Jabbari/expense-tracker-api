# Use the official Python 3.9 slim image as base
FROM python:3.9-slim

# Prevent Python from writing pyc files to disc and enable stdout/stderr logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY . /app/

# Expose port 8000 for the application
EXPOSE 8000

# Use Gunicorn to serve the Django app
CMD ["gunicorn", "expense_tracker_api.wsgi:application", "--bind", "0.0.0.0:8000"]
