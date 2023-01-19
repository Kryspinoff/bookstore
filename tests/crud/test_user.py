from app import crud, models
from app.constants import Role
from app.core.security import verify_password
from app.schemas.user import UserCreateInDB, UserUpdate
from fastapi.encoders import jsonable_encoder
import pytest
from sqlalchemy.orm import Session
from tests.utils.utils import (
    random_valid_email, random_valid_first_name, random_valid_last_name,
    random_valid_phone_number, random_valid_username
)


def test_create_user(db_user: models.User) -> None:
    assert db_user.first_name == "William"
    assert db_user.last_name == "Smith"
    assert db_user.username == "william_smith"
    assert db_user.email == "william.smith@email.com"
    assert db_user.phone_number == "48999999999"
    assert db_user.role == Role.USER
    assert verify_password("Secret#password1", db_user.hashed_password)
    assert db_user.is_active
    assert db_user.books == []
    assert db_user.reviews == []
    assert db_user.wishlist is None
    assert db_user.orders == []


def test_get_user_by_email(db: Session, db_user: models.User) -> None:
    user_2 = crud.user.get_by_email(db, email=db_user.email)
    assert user_2
    assert db_user.id == user_2.id
    assert jsonable_encoder(db_user) == jsonable_encoder(user_2)


def test_get_user_by_id(db: Session, db_user: models.User) -> None:
    user_2 = crud.user.get(db, id=db_user.id)
    assert user_2
    assert db_user.email == user_2.email
    assert jsonable_encoder(db_user) == jsonable_encoder(user_2)


def test_get_user_by_username(db: Session, db_user: models.User) -> None:
    user_2 = crud.user.get_by_username(db, username=db_user.username)
    assert user_2
    assert db_user.username == user_2.username
    assert jsonable_encoder(db_user) == jsonable_encoder(user_2)


def test_get_users(db: Session, db_user: models.User) -> None:
    users = crud.user.get_multi(db)
    assert users[-1] == db_user


@pytest.mark.parametrize(
    "email, username",
    [
        ("william.smith@email.com", None),
        (None, "william_smith")
    ]
)
def test_authenticate_user(db: Session, db_user: models.User, email: str, username: str) -> None:
    authenticated_user = crud.user.authenticate(db, email=email, username=username, password="Secret#password1")
    assert authenticated_user


@pytest.mark.parametrize(
    "email, username, password",
    [
        ("william.smith@email.com", None, "Pa$$word3"),
        (None, "william_smith", "Pa$$word3"),
        (None, random_valid_username(), "Pa$$word3"),
        (random_valid_email(), None, "Pa$$word3"),
        (None, None, "Pa$$word3")
    ]
)
def test_authenticate_user_invalid_data(
    db: Session,
    db_user: models.User,
    email: str,
    username: str,
    password: str
) -> None:
    authenticated_user = crud.user.authenticate(db, email=email, username=username, password=password)
    assert authenticated_user is None


def test_check_if_user_is_active(db: Session, db_user: models.User) -> None:
    assert db_user.is_active


@pytest.mark.parametrize(
    "field, value",
    [
        ("first_name", random_valid_first_name()),
        ("last_name", random_valid_last_name()),
        ("username", random_valid_username()),
        ("email", random_valid_email()),
        ("phone_number", random_valid_phone_number())
    ]
)
def test_update_user_with_schema(db: Session, db_user: models.User, field: str, value: str) -> None:
    user_in_update = UserUpdate(**{field: value})
    user_updated = crud.user.update(db, db_obj=db_user, obj_in=user_in_update)
    assert db_user == user_updated


@pytest.mark.parametrize(
    "field, value",
    [
        ("first_name", random_valid_first_name()),
        ("last_name", random_valid_last_name()),
        ("username", random_valid_username()),
        ("email", random_valid_email()),
        ("phone_number", random_valid_phone_number())
    ]
)
def test_update_user_with_dict(db: Session, db_user: models.User, field: str, value: str) -> None:
    user_in_update = {field: value}
    user_updated = crud.user.update(db, db_obj=db_user, obj_in=user_in_update)
    assert db_user == user_updated


def test_update_password(db: Session, db_user: models.User) -> None:
    new_password = "Pa$$word3"
    user_updated = crud.user.update(db, db_obj=db_user, obj_in={"password": new_password})
    assert db_user.id == user_updated.id
    assert verify_password(new_password, user_updated.hashed_password)


def test_delete_user(db: Session) -> None:
    user_in = UserCreateInDB(
        first_name=random_valid_first_name(),
        last_name=random_valid_last_name(),
        username=random_valid_username(),
        email=random_valid_email(),
        password="Pa$$word3",
        role=Role.USER
    )
    user = crud.user.create(db, obj_in=user_in)
    assert user
    crud.user.remove(db, db_obj=user)
    user = crud.user.get(db, id=user.id)
    assert user is None
