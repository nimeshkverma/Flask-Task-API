# Flask Task Management API

A production-grade REST API for task management built with Flask, featuring JWT authentication, role-based access control, rate limiting, and comprehensive documentation.

## Features

- 🔐 JWT-based authentication
- 👥 Role-based authorization (Admin/User)
- 📝 Full CRUD operations for tasks
- ⚡ Rate limiting (100 requests/hour)
- 📊 Structured JSON logging
- 📚 Swagger/OpenAPI documentation
- ✅ Global error handling
- 🔧 Environment-based configuration
- 📱 User-friendly API design
- 🏗️ Modular architecture

## Project Structure

```
flask-task-api/
├── app/
│   ├── config/
│   │   └── config.py
│   ├── models/
│   │   ├── task.py
│   │   └── user.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── task_routes.py
│   │   └── health_routes.py
│   └── services/
│       ├── auth_service.py
│       └── task_service.py
├── tests/
├── migrations/
├── app.py
├── requirements.txt
└── .env.example
```

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd flask-task-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp .env.example .env
```
   Edit the .env file with your configuration values.

5. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Run the application:
```bash
python app.py
```

## API Endpoints

### Authentication

#### Register a new user
```bash
curl -X POST http://localhost:5001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### Tasks

#### Get all tasks
```bash
curl -X GET http://localhost:5001/api/v1/tasks \
  -H "Authorization: Bearer <your-jwt-token>"
```

#### Get a specific task
```bash
curl -X GET http://localhost:5001/api/v1/tasks/1 \
  -H "Authorization: Bearer <your-jwt-token>"
```

#### Create a task
```bash
curl -X POST http://localhost:5001/api/v1/tasks \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the API implementation",
    "status": "pending",
    "priority": "medium",
    "due_date": "2024-12-31T23:59:59"
  }'
```

#### Update a task
```bash
curl -X PUT http://localhost:5001/api/v1/tasks/1 \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

#### Delete a task
```bash
curl -X DELETE http://localhost:5001/api/v1/tasks/1 \
  -H "Authorization: Bearer <your-jwt-token>"
```

### Admin Endpoints

#### Get all tasks (Admin only)
```bash
curl -X GET http://localhost:5001/api/v1/admin/tasks \
  -H "Authorization: Bearer <your-jwt-token>"
```

### Health Check

```bash
curl -X GET http://localhost:5001/api/v1/health
```

## Authentication Flow

1. Users register with username, email, and password
2. Users login with credentials and receive a JWT token
3. Include the JWT token in the Authorization header for protected endpoints
4. Tokens expire after 1 hour (configurable)

## Rate Limiting

- Default rate limit: 100 requests per hour per IP
- Custom limits can be configured in .env file
- Rate limit headers included in responses

## Error Handling

All errors return JSON responses with this structure:
```json
{
  "error": "Error Type",
  "message": "Detailed error message"
}
```

Common HTTP status codes:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## Extending the Application

### Adding New Models
1. Create new model in `app/models/`
2. Create migrations: `flask db migrate -m "Add new model"`
3. Apply migrations: `flask db upgrade`

### Adding New Routes
1. Create new route file in `app/routes/`
2. Create corresponding service in `app/services/`
3. Register blueprint in `app.py`

### Custom Rate Limits
```python
@limiter.limit("200/day")
def your_route():
    pass

