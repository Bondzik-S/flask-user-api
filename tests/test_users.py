"""Tests for user-related endpoints."""

import pytest
from flask import Flask
from flask.testing import FlaskClient

from flask_user_api import create_app, db
from flask_user_api.config import TestConfig


@pytest.fixture
def app() -> Flask:
    """Create a Flask application configured for testing.

    Returns:
        Flask application instance with in-memory SQLite database.
    """
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for the Flask application.

    Args:
        app: Flask application instance.

    Returns:
        Test client for making requests.
    """
    return app.test_client()


def test_create_user(client: FlaskClient) -> None:
    """Test user creation with valid data."""
    response = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"


def test_create_user_invalid_content_type(client: FlaskClient) -> None:
    """Test user creation with invalid content type."""
    response = client.post(
        "/users",
        data="name=Test&email=test@example.com",
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code == 415


def test_create_user_missing_fields(client: FlaskClient) -> None:
    """Test user creation with missing required fields."""
    response = client.post("/users", json={"name": "Only Name"})
    assert response.status_code == 400


def test_get_users(client: FlaskClient) -> None:
    """Test getting all users."""
    client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    response = client.get("/users")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_nonexistent_user(client: FlaskClient) -> None:
    """Test getting a user that doesn't exist."""
    response = client.get("/users/9999")
    assert response.status_code == 404


def test_get_user_by_id(client: FlaskClient) -> None:
    """Test getting a specific user by ID."""
    create_response = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    user_id = create_response.get_json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == user_id


def test_update_user(client: FlaskClient) -> None:
    """Test updating a user's information."""
    create_response = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    user_id = create_response.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"name": "Updated Name"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Updated Name"
    assert data["email"] == "test@example.com"


def test_update_nonexistent_user(client: FlaskClient) -> None:
    """Test updating a user that doesn't exist."""
    response = client.put("/users/9999", json={"name": "Updated Name"})
    assert response.status_code == 404


def test_delete_user(client: FlaskClient) -> None:
    """Test deleting a user."""
    create_response = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    user_id = create_response.get_json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_user(client: FlaskClient) -> None:
    """Test deleting a user that doesn't exist."""
    response = client.delete("/users/9999")
    assert response.status_code == 404
