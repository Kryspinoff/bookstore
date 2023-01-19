from app.core.config import settings
settings.load_env_file(".env.test")

from datetime import datetime, timedelta
from typing import Generator

from alembic import command
from alembic.config import Config
from app import crud, models, schemas
from app.api.deps import get_db, get_async_db
from app.constants import Role
from app.core.security import get_password_hash
from app.db.session import SessionLocal, engine, AsyncSessionLocal
from app.main import app
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import ObjectDeletedError
from sqlalchemy_utils import database_exists, create_database, drop_database
import pytest
from tests.utils.user import *


@pytest.fixture(scope="module", autouse=True)
def create_test_database():
    assert not database_exists(engine.url), f'Test database already exists. Aborting tests. {engine.url}'
    create_database(engine.url)       # Create the test database.
    config = Config("alembic.ini")
    command.upgrade(config, "head")   # Run the migrations.
    yield                             # Run the tests.
    drop_database(engine.url)


def override_get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def async_override_get_db():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_async_db] = async_override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def user_auth_header() -> dict[str, str]:
    # Creating regular user for tests.
    user_in = models.User(
        username=regular_user_username,
        email=regular_user_email,
        first_name=regular_user_first_name,
        last_name=regular_user_last_name,
        hashed_password=get_password_hash(regular_user_password),
        phone_number=regular_user_phone_number,
        role=Role.USER
    )
    db = SessionLocal()
    db_user = db.query(models.User).filter(models.User.username == regular_user_username).first()
    if not db_user:
        db.add(user_in)
        db.commit()
    db.close()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire,
        "sub": regular_user_username,
        "role": Role.USER
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    yield {"Authorization": f"Bearer {encoded_jwt}"}
    db = SessionLocal()
    db.delete(user_in)
    try:
        db.commit()
    except ObjectDeletedError:
        pass
    finally:
        db.close()


@pytest.fixture(scope="function")
def admin_auth_header() -> dict[str, str]:
    # Creating user admin for tests.
    user_in = models.User(
        username=regular_admin_username,
        email=regular_admin_email,
        first_name=regular_admin_first_name,
        last_name=regular_admin_last_name,
        hashed_password=get_password_hash(regular_admin_password),
        phone_number=regular_admin_phone_number,
        role=Role.ADMIN
    )
    db = SessionLocal()
    db_user = db.query(models.User).filter(models.User.username == regular_admin_username).first()
    if not db_user:
        db.add(user_in)
        db.commit()
    db.close()

    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire,
        "sub": regular_admin_username,
        "role": Role.ADMIN
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    yield {"Authorization": f"Bearer {encoded_jwt}"}
    db = SessionLocal()
    db.delete(user_in)
    db.commit()
    db.close()


@pytest.fixture(scope="function")
def super_admin_auth_header() -> dict[str, str]:
    # Creating super admin for tests.
    user_in = models.User(
        username=regular_super_admin_username,
        email=regular_super_admin_email,
        first_name=regular_super_admin_first_name,
        last_name=regular_super_admin_last_name,
        hashed_password=get_password_hash(regular_super_admin_password),
        phone_number=regular_super_admin_phone_number,
        role=Role.SUPER_ADMIN
    )
    db = SessionLocal()
    db_user = db.query(models.User).filter(models.User.username == regular_super_admin_username).first()
    if not db_user:
        db.add(user_in)
        db.commit()
    db.close()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire,
        "sub": regular_super_admin_username,
        "role": Role.SUPER_ADMIN
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    yield {"Authorization": f"Bearer {encoded_jwt}"}
    db = SessionLocal()
    db.delete(user_in)
    db.commit()
    db.close()


@pytest.fixture(scope="session")
def wrong_auth_header() -> dict[str, str]:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire,
        "sub": regular_super_admin_username,
        "role": Role.SUPER_ADMIN
    }
    encoded_jwt = jwt.encode(
        to_encode, "abc", algorithm=settings.ALGORITHM
    )
    return {"Authorization": f"Bearer {encoded_jwt}"}


@pytest.fixture(scope="function")
def db_author(db: Session) -> models.Author:
    author_in = schemas.AuthorCreate(
        fullname="Test author"
    )
    db_author = crud.author.create_if_not_exists(db, obj_in=author_in)
    yield db_author
    crud.author.remove(db, db_obj=db_author)


@pytest.fixture(scope="function")
def db_genre(db: Session) -> models.Genre:
    genre_in = schemas.GenreCreate(
        name="Test-Genre"
    )
    db_genre = crud.genre.create_if_not_exists(db, obj_in=genre_in)
    yield db_genre
    crud.genre.remove(db, db_obj=db_genre)


@pytest.fixture(scope="function")
def db_book_image(db: Session) -> models.BookImage:
    book_image = schemas.FileCreate(
        filename="Test image book.jpg",
        content_type="image/jpeg"
    )
    db_book_image = crud.book_image.create(db, obj_in=book_image)
    yield db_book_image
    crud.book_image.remove(db, db_obj=db_book_image)


@pytest.fixture(scope="function")
def db_pdf(db: Session) -> models.PDFFile:
    pdf_in = schemas.FileCreate(
        filename="Test full book.pdf",
        content_type="application/pdf"
    )
    db_pdf = crud.pdf_file.create(db, obj_in=pdf_in)
    yield db_pdf
    crud.pdf_file.remove(db, db_obj=db_pdf)


@pytest.fixture(scope="function")
def db_short_pdf(db: Session) -> models.ShortPDFFile:
    short_pdf_in = schemas.FileCreate(
        filename="Test short book.pdf",
        content_type="application/pdf"
    )
    db_short_pdf = crud.short_pdf_file.create(db, obj_in=short_pdf_in)
    yield db_short_pdf
    crud.short_pdf_file.remove(db, db_obj=db_short_pdf)


@pytest.fixture(scope="function")
def db_book(db: Session) -> models.Book:
    book_in = schemas.BookCreate(
        title="Think again: the power of knowing what you don't know",
        description="Lorem ipsum dolor sit amet",
        language="Polish",
        price=0,
        publication_date="2019-09-11",
        isbn="9780593395783",
    )
    book_in = models.Book(**book_in.dict(exclude_unset=True))
    db_book = crud.book.create(db, obj_in=book_in)
    yield db_book
    crud.book.remove(db, db_obj=db_book)


@pytest.fixture(scope="function")
def db_book_with_author_and_genre(
    db: Session,
    db_book: models.Book,
    db_author: models.Author,
    db_genre: models.Genre
) -> models.Book:
    db_book.authors.append(db_author)
    db_book.genres.append(db_genre)
    db.commit()
    yield db_book


@pytest.fixture(scope="function")
def db_book_with_all_attributes(
    db: Session,
    db_book_with_author_and_genre: models.Book,
    db_book_image: models.BookImage,
    db_pdf: models.PDFFile,
    db_short_pdf: models.ShortPDFFile
) -> models.Book:
    db_book_with_author_and_genre.image = db_book_image
    db_book_with_author_and_genre.pdf = db_pdf
    db_book_with_author_and_genre.short_pdf = db_short_pdf
    db.commit()
    yield db_book_with_author_and_genre


@pytest.fixture(scope="function")
def db_user(db: Session) -> schemas.User:
    user_in = schemas.UserCreateInDB(
        first_name="William",
        last_name="Smith",
        username="william_smith",
        email="william.smith@email.com",
        password="Secret#password1",
        phone_number="48999999999",
        role=Role.USER
    )
    db_user = crud.user.create(db, obj_in=user_in)
    yield db_user
    crud.user.remove(db, db_obj=db_user)


@pytest.fixture(scope="function")
def db_user_inactive(db: Session, db_user: models.User) -> schemas.User:
    db_user.is_active = False
    db.commit()
    yield db_user


@pytest.fixture(scope="function")
def db_review(db: Session, db_book: models.Book, db_user: models.User) -> schemas.Review:
    review_in = schemas.ReviewCreate(
        comment="Ok",
        rating=3
    )
    review_in = models.Review(**review_in.dict(exclude_unset=True))
    review_in.book = db_book
    review_in.user = db_user
    db_review = crud.review.create(db, obj_in=review_in)
    yield db_review
    db_review = crud.review.get(db, id=db_review.id)
    if db_review:
        crud.review.remove(db, db_obj=db_review)


@pytest.fixture(scope="function")
def db_wishlist(db: Session, db_book: models.Book, db_user: models.User) -> schemas.Wishlist:
    db_wishlist = crud.toggle.wishlist_book(db, book=db_book, user=db_user)
    yield db_wishlist
    crud.toggle.wishlist_book(db, book=db_book, user=db_user)
