from app import models
from app.core.config import settings
from tests.utils.user import *
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from tests.utils.utils import random_valid_email, random_valid_password, random_valid_username


@pytest.mark.parametrize(
    "username, password",
    [
        (regular_user_email, regular_user_password),
        (regular_user_username, regular_user_password)
    ]
)
def test_login(client: TestClient, db: Session, user_auth_header: dict[str, str], username: str, password: str) -> None:
    data = {
        "username": username,
        "password": password
    }
    response = client.post(
        f"{settings.API_V1_STR}/login/",
        data=data
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    access_token = data["access_token"]

    response = client.get(
        f"{settings.API_V1_STR}/dev/auth_required",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text


@pytest.mark.parametrize(
    "username, password",
    [
        (random_valid_email(), random_valid_password()),
        (random_valid_username(), random_valid_password())
    ]
)
def test_login_user_not_exists(client: TestClient, username: str, password: str) -> None:
    data = {
        "username": username,
        "password": password
    }
    response = client.post(
        f"{settings.API_V1_STR}/login",
        data=data
    )
    assert response.status_code == 400, response.test


def test_login_inactive_user(client: TestClient, db_user_inactive: models.User) -> None:
    data = {
        "username": "william_smith",
        "password": "Secret#password1"
    }
    response = client.post(
        f"{settings.API_V1_STR}/login",
        data=data
    )
    assert response.status_code == 400, response.text
