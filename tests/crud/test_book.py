from datetime import datetime

from app import crud, models, schemas
from sqlalchemy.orm import Session


def test_create_book(db: Session, db_book: models.Book) -> None:
    assert db_book.title == "Think again: the power of knowing what you don't know"
    assert db_book.description == "Lorem ipsum dolor sit amet"
    assert db_book.language == "Polish"
    assert db_book.price == 0
    assert db_book.publication_date == datetime.strptime("2019-09-11", "%Y-%m-%d").date()
    assert db_book.isbn == "9780593395783"
    assert db_book.authors == []
    assert db_book.avg_rating is None
    assert db_book.genres == []
    assert db_book.image is None
    assert db_book.owners == []
    assert db_book.pdf is None
    assert db_book.reviews == []
    assert db_book.short_pdf is None
    assert db_book.wishlists == []


def test_get_book_by_title(db: Session, db_book: models.Book) -> None:
    book_2 = crud.book.get_by_title(db, title="Think again: the power of knowing what you don't know")
    assert db_book == book_2


def test_add_genres(db: Session, db_book: models.Book, db_genre: models.Genre) -> None:
    db_book.genres.append(db_genre)
    db.commit()
    db_book_2 = crud.book.get_by_title(db, title="Think again: the power of knowing what you don't know")
    assert db_book_2.genres == [db_genre]


def test_add_authors(db: Session, db_book: models.Book, db_author: models.Author) -> None:
    db_book.authors.append(db_author)
    db.commit()
    db_book_2 = crud.book.get_by_title(db, title="Think again: the power of knowing what you don't know")
    assert db_book_2.authors == [db_author]


def test_add_image(db: Session, db_book: models.Book, db_book_image: models.BookImage) -> None:
    db_book.image = db_book_image
    db.commit()
    db_book_2 = crud.book.get_by_title(db, title="Think again: the power of knowing what you don't know")
    assert db_book_2.image == db_book_image


def test_add_pdf(db: Session, db_book: models.Book, db_pdf: models.PDFFile) -> None:
    db_book.pdf = db_pdf
    db.commit()
    db_book_2 = crud.book.get_by_title(db, title="Think again: the power of knowing what you don't know")
    assert db_book_2.pdf == db_pdf


def test_add_short_pdf(db: Session, db_book: models.Book, db_short_pdf: models.ShortPDFFile) -> None:
    db_book.short_pdf = db_short_pdf
    db.commit()
    db_book_2 = crud.book.get_by_title(db, title="Think again: the power of knowing what you don't know")
    assert db_book_2.short_pdf == db_short_pdf


def test_update_book(db: Session, db_book: models.Book) -> None:
    book_in = schemas.BookUpdate(
        title="New think again: the power of knowing what you don't know",
        description="New lorem ipsum dolor sit amet",
        language="English",
        price=10.20,
        publication_date="2023-01-01",
        isbn="9999999999999",
    )
    book_2 = crud.book.update(db, db_obj=db_book, obj_in=book_in)
    assert book_2.title == "New think again: the power of knowing what you don't know"
    assert book_2.description == "New lorem ipsum dolor sit amet"
    assert book_2.language == "English"
    assert book_2.price == 10.20
    assert book_2.publication_date == datetime.strptime("2023-01-01", "%Y-%m-%d").date()
    assert book_2.isbn == "9999999999999"
