from tests.utils.user import *
from app import crud, models
from app.core.config import settings
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_update_review(
    client: TestClient, db: Session, user_auth_header: dict[str, str], db_review: models.Review
) -> None:
    db_user = crud.user.get_by_username(db, username=regular_user_username)
    db_review.user = db_user
    db.commit()
    review_id = db_review.id
    data = {
        "comment": "Great book!",
        "rating": 5
    }
    response = client.put(
        f"{settings.API_V1_STR}/reviews/{review_id}",
        headers=user_auth_header,
        json=data
    )
    assert response.status_code == 200, response.text


def test_update_review_not_found(client: TestClient, user_auth_header: dict[str, str]) -> None:
    data = {
        "comment": "Great book!",
        "rating": 5
    }
    response = client.put(
        f"{settings.API_V1_STR}/reviews/100",
        headers=user_auth_header,
        json=data
    )
    assert response.status_code == 404, response.text


def test_delete_review_by_owner(
    client: TestClient, db: Session, user_auth_header: dict[str, str], db_review: models.Review
) -> None:
    db_user = crud.user.get_by_username(db, username=regular_user_username)
    db_review.user = db_user
    db.commit()
    review_id = db_review.id
    response = client.delete(
        f"{settings.API_V1_STR}/reviews/{review_id}",
        headers=user_auth_header
    )
    assert response.status_code == 200, response.text


def test_delete_review_by_user_no_found(
    client: TestClient, db: Session, user_auth_header: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/reviews/100",
        headers=user_auth_header
    )
    assert response.status_code == 404, response.text


def test_delete_review_by_user_unauthorized(
    client: TestClient, db: Session, user_auth_header: dict[str, str], db_review: models.Review
) -> None:
    review_id = db_review.id
    response = client.delete(
        f"{settings.API_V1_STR}/reviews/{review_id}",
        headers=user_auth_header
    )
    assert response.status_code == 403, response.text


def test_delete_review_by_admin(
    client: TestClient, db: Session, admin_auth_header: dict[str, str], db_review: models.Review
) -> None:
    db_user = crud.user.get_by_username(db, username=regular_user_username)
    db_review.user = db_user
    db.commit()
    review_id = db_review.id
    response = client.delete(
        f"{settings.API_V1_STR}/reviews/{review_id}",
        headers=admin_auth_header
    )
    assert response.status_code == 200, response.text


def test_delete_review_by_admin_no_found(
    client: TestClient, db: Session, admin_auth_header: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/reviews/100",
        headers=admin_auth_header
    )
    assert response.status_code == 404, response.text
