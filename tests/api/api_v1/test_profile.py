from app import crud, schemas
from app.constants import Role
from app.core.config import settings
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from tests.utils.user import *
from tests.utils.utils import (
    random_valid_email, random_valid_first_name, random_valid_last_name,
    random_valid_password, random_valid_phone_number, random_valid_username
)


@pytest.fixture()
def random_db_user(client: TestClient, db: Session) -> dict[str, str]:
    user_in = schemas.UserInDB(
        username=random_valid_username(),
        email=random_valid_email(),
        first_name=random_valid_first_name(),
        last_name=random_valid_last_name(),
        password=random_valid_password(),
        phone_number=random_valid_phone_number(),
        role=Role.USER
    )
    db_user = crud.user.create(db, obj_in=user_in)
    yield db_user
    crud.user.remove(db, db_user)


def test_get_current_user(client: TestClient, user_auth_header: dict[str, str]) -> None:
    response = client.get(f"{settings.API_V1_STR}/profile", headers=user_auth_header)
    assert response.status_code == 200, response.text
    current_user = response.json()
    assert current_user
    assert current_user["email"] == regular_user_email
    assert current_user["username"] == regular_user_username
    assert current_user["first_name"] == regular_user_first_name
    assert current_user["last_name"] == regular_user_last_name
    assert current_user["phone_number"] == regular_user_phone_number


def test_get_user_library(client: TestClient, user_auth_header: dict[str, str]) -> None:
    response = client.get(f"{settings.API_V1_STR}/profile/library", headers=user_auth_header)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_get_user_wishlist(client: TestClient, user_auth_header: dict[str, str]) -> None:
    response = client.get(f"{settings.API_V1_STR}/profile/wishlist", headers=user_auth_header)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data is None


def test_set_new_password(client: TestClient, user_auth_header: dict[str, str]) -> None:
    response = client.patch(
        f"{settings.API_V1_STR}/profile/set_new_password",
        headers=user_auth_header,
        json={
            "password": regular_user_password,
            "new_password": "new" + regular_user_password
        }
    )
    assert response.status_code == 200, response.text


def test_set_new_password_invalid_data(client: TestClient, user_auth_header: dict[str, str]) -> None:
    response = client.patch(
        f"{settings.API_V1_STR}/profile/set_new_password",
        headers=user_auth_header,
        json={
            "password": regular_user_password,
            "new_password": "pass"
        }
    )
    assert response.status_code == 422, response.text


def test_set_new_password_wrong_old_password(client: TestClient, user_auth_header: dict[str, str]) -> None:
    response = client.patch(
        f"{settings.API_V1_STR}/profile/set_new_password",
        headers=user_auth_header,
        json={
            "password": "wrongOldPassword%3",
            "new_password": regular_user_password
        }
    )
    assert response.status_code == 400, response.text


def test_set_new_password_repeated(client: TestClient, user_auth_header: dict[str, str]) -> None:
    response = client.patch(
        f"{settings.API_V1_STR}/profile/set_new_password",
        headers=user_auth_header,
        json={
            "password": regular_user_password,
            "new_password": regular_user_password
        }
    )
    assert response.status_code == 400, response.text


@pytest.mark.parametrize(
    "field, new_value",
    [
        ("first_name", "new " + regular_user_first_name),
        ("last_name", "new " + regular_user_last_name),
        ("username", "new_" + regular_user_username),
        ("email", "new-" + regular_user_email),
        ("phone_number", "48600600702")
    ]
)
def test_update_user(
        client: TestClient,
        user_auth_header: dict[str, str],
        field: str,
        new_value: str
) -> None:
    response = client.patch(f"{settings.API_V1_STR}/profile", headers=user_auth_header, json={field: new_value})
    assert response.status_code == 200, response.text
    data = response.json()
    assert new_value == data[field]


@pytest.mark.parametrize(
    "field, new_value",
    [
        ("first_name", "Invalid1Name"),
        ("last_name", "Invalid2Name"),
        ("username", "Invalid-Name"),
        ("email", "Invalid..email.com"),
        ("phone_number", "Invalid.Number")
    ]
)
def test_update_user_invalid_data(
        client: TestClient,
        user_auth_header: dict[str, str],
        field: str,
        new_value: str
) -> None:
    response = client.patch(f"{settings.API_V1_STR}/profile", headers=user_auth_header, json=({field: new_value}))
    assert response.status_code == 422, response.text


def test_update_username_already_used(
        client: TestClient,
        user_auth_header: dict[str, str],
        admin_auth_header: dict[str, str]
) -> None:
    response = client.patch(
        f"{settings.API_V1_STR}/profile",
        headers=user_auth_header,
        json={"username": regular_admin_username}
    )
    assert response.status_code == 409, response.text


def test_update_email_already_used(
        client: TestClient,
        user_auth_header: dict[str, str],
        admin_auth_header: dict[str, str]
) -> None:
    response = client.patch(
        f"{settings.API_V1_STR}/profile",
        headers=user_auth_header,
        json={"email": regular_admin_email}
    )
    assert response.status_code == 409, response.text


def test_delete_profile(
        client: TestClient,
        user_auth_header: dict[str, str],
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/profile",
        headers=user_auth_header,
        params={"password": regular_user_password}
    )
    assert response.status_code == 200, response.text


def test_delete_profile_invalid_password(
        client: TestClient,
        user_auth_header: dict[str, str],
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/profile",
        headers=user_auth_header,
        params={"password": regular_user_password + "a"}
    )
    assert response.status_code == 400, response.text


def test_delete_profile_invalid_data(
        client: TestClient,
        user_auth_header: dict[str, str],
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/profile",
        headers=user_auth_header,
        params={"password": "Pa$$word"}
    )
    assert response.status_code == 422, response.text
