from app import models
from app.core.config import settings
from fastapi.testclient import TestClient
from uuid import uuid4


def test_get_users(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/users",
        headers=admin_auth_header
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)


def test_get_user_by_id(client: TestClient, admin_auth_header: dict[str, str], db_user: models.User) -> None:
    user_id = db_user.id
    response = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=admin_auth_header
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == db_user.username


def test_set_role(client: TestClient, super_admin_auth_header: dict[str, str], db_user: models.User) -> None:
    user_id = db_user.id
    response = client.patch(
        f"{settings.API_V1_STR}/users/{user_id}/set_role",
        headers=super_admin_auth_header,
        params={"role": "ADMIN"}
    )
    assert response.status_code == 200, response.text


def test_set_role_user_not_found(client: TestClient, super_admin_auth_header: dict[str, str]) -> None:
    response = client.patch(
        f"{settings.API_V1_STR}/users/{uuid4()}/set_role",
        headers=super_admin_auth_header,
        params={"role": "ADMIN"}
    )
    assert response.status_code == 404, response.text
