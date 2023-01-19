from app.core.config import settings
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from tests.utils.user import *
from tests.utils.utils import (
    random_valid_email, random_valid_first_name, random_valid_last_name,
    random_valid_phone_number, random_valid_username
)


def test_create_user(client: TestClient, db: Session) -> None:
    data = {
        "username": "testuser",
        "email": "testuser@email.com",
        "first_name": "test",
        "last_name": "test",
        "password": "Pa$$word5",
        "phone_number": "48999000999"
    }
    response = client.post(f"{settings.API_V1_STR}/register", json=data)
    assert response.status_code == 201, response.text
    response_data = response.json()
    assert response_data["access_token"]
    assert response_data["token_type"] == "bearer"


def test_create_user_missing_data(client: TestClient) -> None:
    data = {
        "username": "testuser2",
        "email": "testuser2@email.com",
        "last_name": "test",
        "password": "Pa$$word5",
        "phone_number": "48999000998"
    }
    response = client.post(f"{settings.API_V1_STR}/register", json=data)
    assert response.status_code == 422, response.text


@pytest.mark.parametrize(
    "username, email",
    [
        (regular_user_username, random_valid_email()),
        (random_valid_username(), regular_user_email)
    ]
)
def test_create_user_username_or_email_already_exist(
    client: TestClient,
    user_auth_header: dict[str, str],
    username: str,
    email: str
) -> None:
    data = {
        "username": username,
        "email": email,
        "first_name": random_valid_first_name(),
        "last_name": random_valid_last_name(),
        "password": "Pa$$word5",
        "phone_number": random_valid_phone_number()
    }
    response = client.post(f"{settings.API_V1_STR}/register", json=data)
    assert response.status_code == 409, response.text
