# Flask User API

Simple REST API for user management built with Flask and PostgreSQL.

## Technologies

- **Python 3.12**
- **Flask**: Web framework
- **PostgreSQL**: Database
- **SQLAlchemy**: ORM
- **Marshmallow**: Serialization/Deserialization
- **Flask-Migrate**: Database migrations
- **Poetry**: Dependency management
- **Docker**: Containerization
- **Swagger UI**: API documentation

## Features

- Create, Read, Update, Delete (CRUD) operations for users
- Input validation
- Error handling
- API documentation
- Docker support
- Database migrations
- CORS support

## API Endpoints

- `POST /users`: Create a new user
- `GET /users`: Get all users
- `GET /users/{id}`: Get user by ID
- `PUT /users/{id}`: Update user
- `DELETE /users/{id}`: Delete user

API documentation is available at `/docs` endpoint when the application is running.

## Local Development

### Prerequisites

- Python 3.12
- Poetry
- PostgreSQL

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Bondzik-S/flask-user-api
cd flask-user-api
```

2. Install dependencies:
```bash
poetry install
```

3. Create `.env` file:
```bash
POSTGRES_DB=flask_user_api_db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=some_password
POSTGRES_HOST=localhost

FLASK_APP=run.py
```

4. Initialize the database:
```bash
poetry run flask db upgrade
```

5. Run the application:
```bash
poetry run flask run
```

The API will be available at `http://localhost:5000`

## Docker Setup

### Prerequisites

- Docker
- Docker Compose

### Running with Docker

1. Clone the repository:
```bash
git clone https://github.com/Bondzik-S/flask-user-api
cd flask-user-api
```

2. Create `.env` file (same as above)

3. Build and start containers:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:5000`

## Testing

Run tests using pytest:

```bash
poetry run pytest
```

## API Documentation

Once the application is running, visit `http://localhost:5000/docs` to view the Swagger UI documentation.