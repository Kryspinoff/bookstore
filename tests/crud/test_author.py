from app import crud, models
from sqlalchemy.orm import Session


def test_create_author_if_not_exists(db: Session, db_author: models.Author):
    assert db_author.fullname == "Test Author"


def test_get_author_by_fullname(db: Session, db_author: models.Author):
    author_2 = crud.author.get_by_fullname(db, fullname="Test Author")
    assert db_author.fullname == author_2.fullname
