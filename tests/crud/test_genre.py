from app import crud, models
from sqlalchemy.orm import Session


def test_create_genre_if_not_exists(db: Session, db_genre: models.Genre):
    assert db_genre.name == "test-genre"


def test_get_genre_by_name(db: Session, db_genre: models.Genre):
    genre_2 = crud.genre.get_by_name(db, name="test-genre")
    assert db_genre.name == genre_2.name
