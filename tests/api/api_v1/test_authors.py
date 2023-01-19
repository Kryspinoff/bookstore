from app import models
from app.core.config import settings
from fastapi.testclient import TestClient


def test_create_author(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "fullname": "Acceptable Name"
    }
    response = client.post(f"{settings.API_V1_STR}/authors", headers=admin_auth_header, json=data)
    assert response.status_code == 201, response.text


def test_create_author_already_exist(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "fullname": "Acceptable Name"
    }
    response = client.post(f"{settings.API_V1_STR}/authors", headers=admin_auth_header, json=data)
    assert response.status_code == 400, response.text


def test_create_author_invalid_data(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "fullname": "$Wrong Name"
    }
    response = client.post(f"{settings.API_V1_STR}/authors", headers=admin_auth_header, json=data)
    assert response.status_code == 422, response.text  # Sprawdź czy ten kod powinieneś gdzies zastosować (api)


def test_get_author(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/authors/1")
    assert response.status_code == 200, response.text


def test_get_authors(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/authors")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["fullname"] == "Acceptable Name"
    assert data[0]["id"] == 1


def test_get_author_failed(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/authors/100")
    assert response.status_code == 404, response.text


def test_update_author(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "fullname": "A. Name"
    }
    response = client.put(f"{settings.API_V1_STR}/authors/1", headers=admin_auth_header, json=data)
    assert response.status_code == 200, response.text


def test_update_author_invalid_data(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "fullname": "Wrong,.. Name"
    }
    response = client.put(f"{settings.API_V1_STR}/authors/1", headers=admin_auth_header, json=data)
    assert response.status_code == 422, response.text


def test_update_author_already_exists(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "fullname": "A. Name"
    }
    response = client.put(f"{settings.API_V1_STR}/authors/100", headers=admin_auth_header, json=data)
    assert response.status_code == 404, response.text


def test_get_author_books_when_book_exists(client: TestClient, db_book_with_all_attributes: models.Book) -> None:
    author_id = db_book_with_all_attributes.authors[0].id
    response = client.get(f"{settings.API_V1_STR}/authors/{author_id}/books")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["title"] == "Think again: the power of knowing what you don't know"
    assert data[0]["authors"][0]["fullname"] == "Test Author"


def test_get_author_books_when_book_not_exists(
    client: TestClient,
    db_book_with_all_attributes: models.Book
) -> None:
    response = client.get(f"{settings.API_V1_STR}/authors/1/books")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_get_author_books_author_not_found(client: TestClient, db_book_with_all_attributes: models.Book) -> None:
    response = client.get(f"{settings.API_V1_STR}/authors/100/books")
    assert response.status_code == 404, response.text


def test_delete_author(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.delete(f"{settings.API_V1_STR}/authors/1", headers=admin_auth_header)
    assert response.status_code == 200, response.text


def test_delete_author_not_found(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.delete(f"{settings.API_V1_STR}/authors/100", headers=admin_auth_header)
    assert response.status_code == 404, response.text
