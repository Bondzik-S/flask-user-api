import pytest
from flask_user_api import create_app, db
from flask_user_api.models import User

@pytest.fixture
def app():
    # Створюємо додаток у режимі тестування з in-memory SQLite базою даних
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"  # in-memory БД для тестування
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_user(client):
    # Тест створення користувача
    response = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"

def test_create_user_invalid_content_type(client):
    """ Перевіряємо, що при неправильному Content-Type сервер повертає 415 """
    response = client.post("/users", data="name=Test&email=test@example.com", headers={"Content-Type": "text/plain"})
    assert response.status_code == 415

def test_create_user_missing_fields(client):
    """ Перевіряємо, що якщо не передати обов’язкові поля, буде 400 """
    response = client.post("/users", json={"name": "Only Name"})
    assert response.status_code == 400

def test_get_users(client):
    # Створюємо користувача для перевірки списку
    client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    response = client.get("/users")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1

def test_get_nonexistent_user(client):
    """ Перевіряємо, що запит на неіснуючого користувача повертає 404 """
    response = client.get("/users/9999")
    assert response.status_code == 404

def test_get_user_by_id(client):
    # Створюємо користувача та отримуємо його ID
    create_response = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    user_id = create_response.get_json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == user_id

def test_update_user(client):
    # Створюємо користувача
    create_response = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    user_id = create_response.get_json()["id"]
    # Оновлюємо ім'я користувача
    response = client.put(f"/users/{user_id}", json={"name": "Updated Name"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Updated Name"
    assert data["email"] == "test@example.com"

def test_update_nonexistent_user(client):
    """ Перевіряємо, що оновлення неіснуючого користувача повертає 404 """
    response = client.put("/users/9999", json={"name": "New Name"})
    assert response.status_code == 404

def test_delete_user(client):
    # Створюємо користувача
    create_response = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    user_id = create_response.get_json()["id"]
    # Видаляємо користувача
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User deleted"
    # Перевіряємо, що користувача більше немає
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_user(client):
    """ Перевіряємо, що видалення неіснуючого користувача повертає 404 """
    response = client.delete("/users/9999")
    assert response.status_code == 404
