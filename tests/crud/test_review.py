from app import crud, models, schemas
from sqlalchemy.orm import Session


def test_create_review(db: Session, db_review: models.Review) -> None:
    assert db_review.user.username == "william_smith"
    assert db_review.book.title == "Think again: the power of knowing what you don't know"
    assert db_review.comment == "Ok"
    assert db_review.rating == 3
    assert db_review.edited is False


def test_get_review_by_user(db: Session, db_review: models.Review) -> None:
    user = crud.user.get_by_username(db, username="william_smith")
    book = crud.book.get_by_title(db, title="Think again: the power of knowing what you don't know")
    review = crud.review.get_by_user(db, user=user, book_id=book.id)
    assert review
    assert review.edited is False


def test_get_review_by_user_not_exists(db: Session, db_user: models.User, db_book: models.Book) -> None:
    review = crud.review.get_by_user(db, user=db_user, book_id=db_book.id)
    assert review is None


def test_update_review(db: Session, db_review: models.Review) -> None:
    review_in = schemas.ReviewCreate(
        comment="Ok update",
        rating=5
    )
    review = crud.review.update(db, db_obj=db_review, obj_in=review_in)
    assert review.comment == "Ok update"
    assert review.rating == 5
    assert review.edited
