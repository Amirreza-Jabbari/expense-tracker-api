
# Expense Tracker API

A RESTful API for managing expenses, built with Django, Django REST Framework, and JWT authentication with PostgreSQL database. Users can sign up, log in, and manage (create, read, update, delete) their own expenses. The API also includes endpoints for filtering expenses by date ranges. Additionally, the project features endpoints to reset users' passwords with email.

This project was built based on one of the inspiring project ideas featured on [roadmap.sh](https://roadmap.sh/backend). You can check out the original concept here: [Expense Tracker API](https://roadmap.sh/projects/expense-tracker-api).

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
  - [With Docker Compose](#With-Docker-Compose)
  - [Running Locally Without Docker](#Running-Locally-Without-Docker)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **User Authentication & Authorization**:  
  - Sign up as a new user.
  - JWT-based authentication for secure API access.
  - Password reset via email.

- **User CRUD**:  
  - Create, retrieve, update, and delete user accounts.

- **Expense Management**:  
  - Create, list (with filtering options), retrieve, update, and delete expense records.
  - Filter expenses by past week, past month, last 3 months, or a custom date range.
  - Expense categories include: Groceries, Leisure, Electronics, Utilities, Clothing, Health, Others.

- **Containerized with Docker**:  
  - Uses a Python Slim image.
  - PostgreSQL as the database.
  - Docker Compose for local development.

## Requirements

- Python (3.9-slim)
- Django & Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- Gunicorn (for production server)

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Amirreza-Jabbari/expense-tracker-api.git
cd expense-tracker-api
```

---

## Running the Application

### With Docker Compose

To build and run all services:

```bash
docker-compose up --build
```

To stop all services:

```bash
docker-compose down
```

The project is configured to run on port 8000.

### Running Locally Without Docker

If running locally:
### 1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 2. Configure Environment Variables:

   Create a `.env` file or set the following environment variables in your shell:
   - `DEBUG=1`
   - `SECRET_KEY=your-secret-key`
   - `DATABASE_NAME=expense_tracker`
   - `DATABASE_USER=postgres`
   - `DATABASE_PASSWORD=postgres`
   - `DATABASE_HOST=localhost`
   - `DATABASE_PORT=5432`

### 3. Apply Migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### 4. create superuser
```bash
python manage.py createsuperuser
```

### 5. Run the Django Server:

   ```bash
   python manage.py runserver
   ```

### 6. **Access the API:**

   Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## API Endpoints

### You can see complete documentation of [Expense Tracker API Endpoints](endpoints.md) in the endpoints.md file.

---

## Testing

API tests for both user and expense endpoints have been implemented using Django's `APITestCase`. To run tests, execute:

```bash
python manage.py test
```

---

## Contributing

Contributions are welcome! Please submit pull requests or open issues. Make sure to update tests and documentation accordingly.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---