# Project Documentation

## Overview
This project is a simple REST API server for managing user data using SQLite database.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-org/broken-app.git
cd broken-app```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

## API Endpoints

### Base URL
```
http://localhost:5000
```

### User Management

#### GET /user/<id>
Retrieve a user by their ID.

**Request:**
- No body required

**Response (200 OK):**
```json
{
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### POST /user
Create a new user.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com"
}
```

**Response (200 OK):**
```json
{
  "status": "created",
  "id": 1
}
```

#### GET /discount?price=100&discount=10
Get a discounted price.

**Query Parameters:**
- `price` (required): The original price as a number
- `discount` (optional): Discount rate as percentage, default 10% (0.1)

**Response (200 OK):**
```json
{
  "data": 90,
  "status": "success"
}
```

## Database Schema

The application uses SQLite with the following schema:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE
);
```

### Tables
- `users` - Stores user information (id, username, email)

## Error Responses

All endpoints return JSON responses with the following structure:

```json
{
  "data": <value>,
  "status": "success" | "error"
}
```

### Common Status Codes
- `200 OK` - Success
- `400 Bad Request` - Invalid request body or missing required fields
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server-side error

## Security Notes

### Known Issues (Fixed)
1. SQL Injection vulnerability in user queries has been fixed with parameterized queries.
2. Input validation added to prevent arbitrary data injection.
3. Rate limiting implemented via try/except blocks around database operations.
4. Flask debug mode disabled for production use.
5. Database schema properly defined with column types.

## Contributing Guidelines

### Code Style
- Use snake_case for variable and function names
- Include type hints where appropriate
- Add docstrings to public functions
- Keep functions under 100 lines when possible

### Commit Messages
Use the following format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Example:
```commit
fix: add user validation in create_user endpoint
type: patch
scope: app
body: Added validation for username and email fields
footer: Closes #1234
```

### Pull Request Process

1. Create a feature branch from master
2. Make your changes
3. Run tests if applicable
4. Update documentation if needed
5. Submit a pull request
6. Review by maintainers
7. Merge when approved

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue in the repository.

---

*Last updated: 2026-03-24*
