from datetime import datetime, timedelta

from app import models
from app.constants import Role
from app.core.config import settings
from fastapi.testclient import TestClient
from jose import jwt
import pytest


@pytest.fixture(
    scope="function",
    params=[
        None,
        Role.USER,
        Role.ADMIN,
        Role.SUPER_ADMIN
    ]
)
def optional_auth(request, db_user: models.User) -> dict[str, str]:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire,
        "sub": db_user.username,
        "role": request.param
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return {"Authorization": f"Bearer {encoded_jwt}"}


def test_auth(
    client: TestClient,
    super_admin_auth_header: dict[str, str],
    admin_auth_header: dict[str, str],
    user_auth_header: dict[str, str]
) -> None:
    path = f"{settings.API_V1_STR}/dev/auth_required"
    response = client.get(path, headers=user_auth_header)
    assert response.status_code == 200, response.text
    response = client.get(path, headers=admin_auth_header)
    assert response.status_code == 200, response.text
    response = client.get(path, headers=super_admin_auth_header)
    assert response.status_code == 200, response.text


def test_auth_unauthorized(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/dev/auth_required")
    assert response.status_code == 401, response.text


def test_auth_forbidden(client: TestClient, wrong_auth_header: dict[str, str]) -> None:
    response = client.get(f"{settings.API_V1_STR}/dev/auth_required", headers=wrong_auth_header)
    assert response.status_code == 403, response.text


def test_auth_optional(client: TestClient, optional_auth: dict[str, str]) -> None:
    response = client.get(f"{settings.API_V1_STR}/dev/auth_optional", headers=optional_auth)
    assert response.status_code == 200, response.text


def test_admin_auth(
    client: TestClient,
    admin_auth_header: dict[str, str],
    super_admin_auth_header: dict[str, str]
) -> None:
    path = f"{settings.API_V1_STR}/dev/admin_required"
    response = client.get(path, headers=admin_auth_header)
    assert response.status_code == 200, response.text
    response = client.get(path, headers=super_admin_auth_header)
    assert response.status_code == 200, response.text


def test_admin_auth_unauthorized(client: TestClient, user_auth_header: dict[str, str]) -> None:
    response = client.get(f"{settings.API_V1_STR}/dev/admin_required", headers=user_auth_header)
    assert response.status_code == 401, response.text


def test_super_admin_auth(client: TestClient, super_admin_auth_header: dict[str, str]) -> None:
    response = client.get(f"{settings.API_V1_STR}/dev/super_admin_required", headers=super_admin_auth_header)
    assert response.status_code == 200, response.text


def test_super_admin_unauthorized(
    client: TestClient,
    admin_auth_header: dict[str, str],
    user_auth_header: dict[str, str]
) -> None:
    path = f"{settings.API_V1_STR}/dev/super_admin_required"
    response = client.get(path, headers=user_auth_header)
    assert response.status_code == 401, response.text
    response = client.get(path, headers=admin_auth_header)
    assert response.status_code == 401, response.text