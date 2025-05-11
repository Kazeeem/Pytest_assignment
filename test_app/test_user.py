import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# The 3 lines of code above help my terminal to locate the main.py file by adjusting the import path so that test_user.py
# can successfully import my app from the main.py file.

from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_user():
    payload = {
        "name": "Johny bravo",
        "email": "johny@gmail.com",
        "username": "kaz",
        "password": "12345678",
        "age": 500,
        "phone": "+23482499099"
    }


    response = client.post("/users/create", json=payload)
    data = response.json()
    assert data["message"] == "User created successfully"
    assert data["data"]["name"] == "Johny bravo"


def test_get_user_by_id():
    payload = {
        "name": "Jon Doe",
        "email": "jondoe@gmail.com",
        "username": "jon",
        "password": "12345678",
        "age": 500,
        "phone": "+23482499099"
    }
    response = client.post("/users/create", json=payload)
    add_user_data = response.json()
    user_id = add_user_data['data']['id']
    get_response = client.get(f"/users/details/{user_id}")
    get_user_data = get_response.json()
    assert get_response.status_code == 200
    assert get_user_data['id'] == user_id


def test_get_user_by_id_not_found():
    user_id = 1
    get_response = client.get(f"/users/details/{user_id}")
    get_user_data = get_response.json()
    assert get_response.status_code == 404
    assert get_user_data['detail'] == "User not found"


def test_update_user():
    payload = {
        "name": "Johny bravo",
        "email": "johny@gmail.com",
        "username": "johny",
        "password": "12345678",
        "age": 500,
        "phone": "+23482499099"
    }

    update_payload = {
        "name": "Kaz the bad guy"
    }

    response = client.post("/users/create", json=payload)
    added_user_data = response.json()
    user_id = added_user_data['data']['id']

    update_response = client.put(f"/users/update/{user_id}", json=update_payload)
    update_data = update_response.json()
    assert update_data["message"] == "User updated successfully"
    assert update_data["data"]["name"] == "Kaz the bad guy"


def test_update_user_failed():
    user_id = str(uuid.uuid4())

    update_payload = {
        "name": "Kaz the bad guy",
    }

    update_response = client.put(f"/users/update/{user_id}", json=update_payload)
    update_data = update_response.json()
    assert update_response.status_code == 404
    assert update_data['detail'] == f"User with id: {user_id} not found"


def test_delete_user():
    payload = {
        "name": "Queen Latifa",
        "email": "queenlatifa@gmail.com",
        "username": "queen",
        "password": "12345678",
        "age": 500,
        "phone": "+23482499099"
    }

    response = client.post("/users/create", json=payload)
    added_user_data = response.json()
    user_id = added_user_data['data']['id']

    update_response = client.delete(f"/users/delete/{user_id}")
    update_data = update_response.json()
    assert update_data["message"] == "User deleted successfully"


def test_user_delete_failed():
    user_id = str(uuid.uuid4())

    delete_response = client.delete(f"/users/delete/{user_id}")
    response = delete_response.json()
    assert delete_response.status_code == 404
    assert response['detail'] == f"User with id: {user_id} not found"


def test_change_password():
    payload = {
        "name": "Queen Latifa",
        "email": "queenlatifa@gmail.com",
        "username": "queen",
        "password": "12345678",
        "age": 500,
        "phone": "+23482499099"
    }

    response = client.post("/users/create", json=payload)
    added_user_data = response.json()
    user_id = added_user_data['data']['id']

    password_payload = {
        "current_password": "12345678",
        "new_password": "123456",
        "confirm_new_password": "123456"
    }

    password_update = client.post(f"/users/change-password/{user_id}", json=password_payload)
    password_data = password_update.json()
    assert password_data["message"] == "Password changed successfully"


def test_invalid_password():
    payload = {
        "name": "Queen Latifa",
        "email": "queenlatifa@gmail.com",
        "username": "queen",
        "password": "12345678",
        "age": 500,
        "phone": "+23482499099"
    }

    response = client.post("/users/create", json=payload)
    added_user_data = response.json()
    user_id = added_user_data['data']['id']

    password_payload = {
        "current_password": "1234",
        "new_password": "123456",
        "confirm_new_password": "123456"
    }

    password_update = client.post(f"/users/change-password/{user_id}", json=password_payload)
    password_data = password_update.json()
    assert password_update.status_code == 422
    assert password_data["detail"] == "Unprocessable entity"


def test_new_and_confirmation_password_mismatch():
    payload = {
        "name": "Queen Latifa",
        "email": "queenlatifa@gmail.com",
        "username": "queen",
        "password": "12345678",
        "age": 500,
        "phone": "+23482499099"
    }

    response = client.post("/users/create", json=payload)
    added_user_data = response.json()
    user_id = added_user_data['data']['id']

    password_payload = {
        "current_password": "12345678",
        "new_password": "123456",
        "confirm_new_password": "12345692370"
    }

    password_update = client.post(f"/users/change-password/{user_id}", json=password_payload)
    password_data = password_update.json()
    assert password_update.status_code == 422
    assert password_data["detail"] == "Unprocessable entity"


def test_user_login():
    payload = {
        "name": "Queen Latifa",
        "email": "jackiechan@gmail.com",
        "username": "jackie",
        "password": "12345678",
        "age": 500,
        "phone": "+23482499099"
    }

    client.post("/users/create", json=payload)

    login_payload = {
        "email": "jackiechan@gmail.com",
        "password": "12345678",
    }

    password_update = client.post(f"/users/login", json=login_payload)
    password_data = password_update.json()
    assert password_data["message"] == "Login successful"


def test_user_login_failed_due_to_wrong_email():
    payload = {
        "name": "Lionel Messi",
        "email": "lionel@gmail.com",
        "username": "messi",
        "password": "12345678",
        "age": 500,
        "phone": "+23482499099"
    }

    client.post("/users/create", json=payload)

    login_payload = {
        "email": "lionelmercy@gmail.com",
        "password": "12345678",
    }

    password_update = client.post(f"/users/login", json=login_payload)
    password_data = password_update.json()
    assert password_update.status_code == 401
    assert password_data["detail"] == "Unauthorized - Invalid login credentials"


def test_user_login_failed_due_to_wrong_password():
    payload = {
        "name": "David Alaba Messi",
        "email": "davidalaba@gmail.com",
        "username": "alaba",
        "password": "12345678",
        "age": 500,
        "phone": "+23482499099"
    }

    client.post("/users/create", json=payload)

    login_payload = {
        "email": "davidalaba@gmail.com",
        "password": "1234",
    }

    password_update = client.post(f"/users/login", json=login_payload)
    password_data = password_update.json()

    assert password_update.status_code == 401
    assert password_data["detail"] == "Unauthorized - Invalid login credentials"
