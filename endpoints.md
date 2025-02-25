# Expense Tracker API Endpoints

---

## Overview

This API uses JWT (JSON Web Tokens) for authentication. Once authenticated, a user can manage their account (via the User endpoints) and handle their own expenses (via the Expense endpoints). Expense filtering is provided via query parameters.

---

## 1. Authentication Endpoints

### 1.1 Obtain JWT Token

**Endpoint:**  
```
POST /api/token/
```

**Description:**  
Obtain an access and refresh token by providing valid credentials.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Example cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword"}'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 1.2 Refresh JWT Token

**Endpoint:**  
```
POST /api/token/refresh/
```

**Description:**  
Refresh the access token using a valid refresh token.

**Request Body:**
```json
{
  "refresh": "your_refresh_token"
}
```

**Example cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'
```

---

## 2. User Endpoints

### 2.1 Create User (Sign Up)

**Endpoint:**  
```
POST /api/user/create/
```

**Description:**  
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "yourpassword",
  "f_name": "FirstName",
  "l_name": "LastName"
}
```

**Example cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/user/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword", "f_name": "FirstName", "l_name": "LastName"}'
```

---

### 2.2 Retrieve User

**Endpoint:**  
```
GET /api/user/get/<email>/
```

**Description:**  
Retrieve details for a specific user identified by email.

**Example cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/user/get/user@example.com/ \
  -H "Authorization: Bearer <your_access_token>"
```

---

### 2.3 List Users

**Endpoint:**  
```
GET /api/user/list/
```

**Description:**  
List all users (requires authentication).

**Example cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/user/list/ \
  -H "Authorization: Bearer <your_access_token>"
```

---

### 2.4 Update User

**Endpoint:**  
```
PATCH /api/user/update/<email>/
```

**Description:**  
Update user information.  
*Note: Use PUT if you want to replace the entire user resource.*

**Request Body (example - partial update):**
```json
{
  "f_name": "UpdatedFirstName",
  "l_name": "UpdatedLastName"
}
```

**Example cURL:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/user/update/user@example.com/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{"f_name": "UpdatedFirstName", "l_name": "UpdatedLastName"}'
```

---

### 2.5 Delete User

**Endpoint:**  
```
DELETE /api/user/delete/<email>/
```

**Description:**  
Delete a specific user.

**Example cURL:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/user/delete/user@example.com/ \
  -H "Authorization: Bearer <your_access_token>"
```

---

### 2.6 Password Reset Request

**Endpoint:**  
```
POST /api/user/password-reset-request/
```

**Description:**  
Initiate a password reset process. An email will be sent with a reset link.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Example cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/user/password-reset-request/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

---

### 2.7 Password Reset Form

**Endpoint:**  
```
GET /api/user/reset-password/
```

**Description:**  
Display a simple HTML form for password reset (typically opened in a browser).

**Example cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/user/reset-password/
```

---

### 2.8 Password Reset Confirm

**Endpoint:**  
```
GET or POST /api/user/reset-password/<uidb64>/<token>/
```

**Description:**  
- **GET:** Display the password reset form.
- **POST:** Submit the new password to reset the account password.

**POST Request Body:**
```json
{
  "token": "<token>",
  "new_password1": "newpassword123",
  "new_password2": "newpassword123"
}
```

**Example cURL (POST):**
```bash
curl -X POST http://127.0.0.1:8000/api/user/reset-password/<uidb64>/<token>/ \
  -H "Content-Type: application/json" \
  -d '{"token": "<token>", "new_password1": "newpassword123", "new_password2": "newpassword123"}'
```

---

## 3. Expense Endpoints

### 3.1 Create a New Expense

**Endpoint:**  
```
POST /api/expenses/
```

**Description:**  
Create a new expense record for the authenticated user.

**Request Body:**
```json
{
  "title": "Grocery Shopping",
  "description": "Bought vegetables and fruits",
  "amount": "45.67",
  "date": "2025-02-20",
  "category": "Groceries"
}
```

**Example cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/expenses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
        "title": "Grocery Shopping",
        "description": "Bought vegetables and fruits",
        "amount": "45.67",
        "date": "2025-02-20",
        "category": "Groceries"
      }'
```

---

### 3.2 List Expenses

**Endpoint:**  
```
GET /api/expenses/
```

**Description:**  
List all expenses for the authenticated user. Supports filtering via query parameters:

- **Filter by Past Month:** `?filter=month`
- **Filter by Past Week:** `?filter=week`
- **Filter by Last 3 Months:** `?filter=3months`
- **Custom Date Range:** `?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

**Example cURL (Past Month Filter):**
```bash
curl -X GET "http://127.0.0.1:8000/api/expenses/?filter=month" \
  -H "Authorization: Bearer <your_access_token>"
```

**Example cURL (Custom Date Range):**
```bash
curl -X GET "http://127.0.0.1:8000/api/expenses/?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Authorization: Bearer <your_access_token>"
```

---

### 3.3 Retrieve a Single Expense

**Endpoint:**  
```
GET /api/expenses/<expense_id>/
```

**Description:**  
Retrieve details for a specific expense owned by the authenticated user.

**Example cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/expenses/1/ \
  -H "Authorization: Bearer <your_access_token>"
```

---

### 3.4 Update an Expense

Expenses can be updated using either PATCH (partial update) or PUT (full update).

#### 3.4.1 Partial Update (PATCH)

**Endpoint:**  
```
PATCH /api/expenses/<expense_id>/
```

**Request Body (example):**
```json
{
  "title": "Updated Grocery Shopping",
  "amount": "50.00"
}
```

**Example cURL:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/expenses/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
        "title": "Updated Grocery Shopping",
        "amount": "50.00"
      }'
```

#### 3.4.2 Full Update (PUT)

**Endpoint:**  
```
PUT /api/expenses/<expense_id>/
```

**Request Body (all required fields):**
```json
{
  "title": "Updated Grocery Shopping",
  "description": "Bought fruits and vegetables in bulk",
  "amount": "50.00",
  "date": "2025-02-20",
  "category": "Groceries"
}
```

**Example cURL:**
```bash
curl -X PUT http://127.0.0.1:8000/api/expenses/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
        "title": "Updated Grocery Shopping",
        "description": "Bought fruits and vegetables in bulk",
        "amount": "50.00",
        "date": "2025-02-20",
        "category": "Groceries"
      }'
```

---

### 3.5 Delete an Expense

**Endpoint:**  
```
DELETE /api/expenses/<expense_id>/
```

**Description:**  
Delete a specific expense record.

**Example cURL:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/expenses/1/ \
  -H "Authorization: Bearer <your_access_token>"
```