import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# The 3 lines of code above help my terminal to locate the main.py file by adjusting the import path so that test_book.py
# can successfully import my app from the main.py file.

from fastapi.testclient import TestClient
from main import app
from schemas.book import BookCreate
import uuid

client = TestClient(app)


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    data = response.json()
    assert data["message"] == "Book added successfully"
    assert data["data"]["title"] == "Johny bravo"


def test_get_book_by_id():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 200
    assert get_book_data['id'] == book_id


def test_get_book_by_id_not_found():
    book_id = 1
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 404
    assert get_book_data['detail'] == "book not found."


def test_update_book():
    payload = {
        "title": "Kaz the bad guy",
        "author": "Kazeem Asifat",
        "year": 2025,
        "pages": 5000,
        "language": "English"
    }

    update_payload = {
        "title": "Python is interesting than PHP",
        "author": "Kaz the bad guy"
    }

    response = client.post("/books", json=payload)
    added_book_data = response.json()
    book_id = added_book_data['data']['id']

    update_response = client.put(f"/books/{book_id}", json=update_payload)
    update_data = update_response.json()
    assert update_data["message"] == "Book updated successfully"
    assert update_data["data"]["title"] == "Python is interesting than PHP"


def test_update_book_failed():
    book_id = str(uuid.uuid4())

    update_payload = {
        "title": "Python is interesting than PHP",
        "author": "Kaz the bad guy"
    }

    update_response = client.put(f"/books/{book_id}", json=update_payload)
    update_data = update_response.json()
    assert update_response.status_code == 404
    assert update_data['detail'] == f"Book with id: {book_id} not found"


def test_delete_book():
    payload = {
        "title": "Kaz the bad guy 2",
        "author": "Kazeem Asifat",
        "year": 2026,
        "pages": 5000,
        "language": "English"
    }

    response = client.post("/books", json=payload)
    added_book_data = response.json()
    book_id = added_book_data['data']['id']

    update_response = client.delete(f"/books/{book_id}")
    update_data = update_response.json()
    assert update_data["message"] == "Book deleted successfully"


def test_book_delete_failed():
    book_id = str(uuid.uuid4())

    delete_response = client.delete(f"/books/{book_id}")
    response = delete_response.json()
    assert delete_response.status_code == 404
    assert response['detail'] == f"Book with id: {book_id} not found"