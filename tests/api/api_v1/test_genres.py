from app import models
from app.core.config import settings
from fastapi.testclient import TestClient


def test_create_genre(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "name": "Acceptable Name"
    }
    response = client.post(
        f"{settings.API_V1_STR}/genres",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "acceptable name"


def test_create_genre_already_exists(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "name": "Acceptable Name"
    }
    response = client.post(
        f"{settings.API_V1_STR}/genres",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 400, response.text


def test_create_genre_invalid_data(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "name": "Unacceptable -Name"
    }
    response = client.post(
        f"{settings.API_V1_STR}/genres",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 422, response.text


def test_get_genre(client: TestClient, db_genre: models.Genre) -> None:
    genre_id = db_genre.id
    response = client.get(f"{settings.API_V1_STR}/genres/{genre_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == db_genre.id
    assert data["name"] == db_genre.name


def test_get_genre_not_found(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/genres/100")
    assert response.status_code == 404, response.text


def test_get_genres(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/genres")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["name"] == "acceptable name"


def test_update_genre(client: TestClient, admin_auth_header: str, db_genre: models.Genre) -> None:
    genre_id = db_genre.id
    data = {
        "name": "Acceptable-Name"
    }
    response = client.put(
        f"{settings.API_V1_STR}/genres/{genre_id}",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == genre_id
    assert data["name"] == "acceptable-name"


def test_update_genre_invalid_data(client: TestClient, admin_auth_header: str, db_genre: models.Genre) -> None:
    genre_id = db_genre.id
    data = {
        "name": "Unacceptable -Name"
    }
    response = client.put(
        f"{settings.API_V1_STR}/genres/{genre_id}",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 422, response.text


def test_update_genre_not_found(client: TestClient, admin_auth_header: str) -> None:
    data = {
        "name": "Acceptable-Name"
    }
    response = client.put(
        f"{settings.API_V1_STR}/genres/100",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 404, response.text


def test_get_genre_books_when_book_exists(client: TestClient, db_book_with_all_attributes: models.Book) -> None:
    genre_id = db_book_with_all_attributes.genres[0].id
    response = client.get(f"{settings.API_V1_STR}/genres/{genre_id}/books")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["title"] == "Think again: the power of knowing what you don't know"
    assert data[0]["genres"][0]["name"] == "test-genre"


def test_get_genre_books_when_book_not_exists(client: TestClient, db_genre: models.Genre) -> None:
    genre_id = db_genre.id
    response = client.get(f"{settings.API_V1_STR}/genres/{genre_id}/books")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_get_genre_books_not_found(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/genres/100/books")
    assert response.status_code == 404, response.text


def test_delete_genre(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.get(f"{settings.API_V1_STR}/genres/")
    data = response.json()
    genre_id = data[0]["id"]
    response = client.delete(
        f"{settings.API_V1_STR}/genres/{genre_id}",
        headers=admin_auth_header
    )
    assert response.status_code == 200, response.text


def test_delete_genre_not_found(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/genres/100",
        headers=admin_auth_header
    )
    assert response.status_code == 404, response.text
