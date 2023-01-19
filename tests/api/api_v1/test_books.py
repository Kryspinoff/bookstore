import os

from app import models, schemas
from app.core.config import settings
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
import pytest

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "tests/data/download")
UPLOAD_DIR = os.path.join(BASE_DIR, "tests/data/upload")
IMAGE_PATH_1 = os.path.join(UPLOAD_DIR, "1.jpg")
IMAGE_PATH_2 = os.path.join(UPLOAD_DIR, "2.jpg")
PDF_FILE_PATH = os.path.join(UPLOAD_DIR, "Lorem ipsum.pdf")
SHORT_PDF_FILE_PATH = os.path.join(UPLOAD_DIR, "Lorem ipsum short.pdf")


@pytest.mark.parametrize(
    "title, authors, genres",
    [
        ("test first title", None, None),
        ("test second title", [{"fullname": "test first author"}, {"fullname": "test second author"}], None),
        ("test third title", None, [{"name": "test first genre"}, {"name": "test-second-genre"}]),
        (
            "test fourth title",
            [{"fullname": "test first author"}, {"fullname": "test second author"}],
            [{"name": "test first genre"}, {"name": "test-second-genre"}]
        ),
    ]
)
def test_create_book(client: TestClient, admin_auth_header: dict[str, str], title, authors, genres) -> None:
    data = {
        "title": title,
        "description": "test description",
        "language": "English",
        "price": 4.12,
        "publication_date": "2005-11-03",
        "isbn": "5305321243234",
    }
    if authors:
        data.update({"authors": authors})
    if genres:
        data.update({"genres": genres})
    response = client.post(
        f"{settings.API_V1_STR}/books",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 201, response.text
    response_data = response.json()
    assert isinstance(response_data, dict)
    for field, value in data.items():
        if isinstance(value, str):
            assert response_data[field] == value
            continue
        if field == "authors":
            for index, element in enumerate(value):
                assert element["fullname"] == authors[index]["fullname"].lower()
            continue
        if field == "genres":
            for index, element in enumerate(value):
                assert element["name"] == genres[index]["name"].lower()
            continue


def test_create_book_already_exists(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "title": "test first title",
        "description": "test description",
        "language": "English",
        "price": 4.12,
        "publication_date": "2005-11-03",
        "isbn": "5305321243234",
    }
    response = client.post(
        f"{settings.API_V1_STR}/books",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 400, response.text


@pytest.mark.parametrize(
    "title, authors, genres",
    [
        ("first duplicate params", [{"fullname": "test first author"}, {"fullname": "test first author"}], None),
        ("second duplicate params", None, [{"name": "test first genre"}, {"name": "test first genre"}]),
        (
            "second duplicate params",
            [{"fullname": "test first author"}, {"fullname": "test first author"}],
            [{"name": "test first genre"}, {"name": "test first genre"}]
        ),
    ]
)
def test_create_book_duplicate_params(
    client: TestClient,
    admin_auth_header: dict[str, str],
    title,
    authors,
    genres
) -> None:
    data = {
        "title": title,
        "description": "test description",
        "language": "English",
        "price": 4.12,
        "publication_date": "2005-11-03",
        "isbn": "5305321243234",
    }
    if authors:
        data.update({"authors": authors})
    if genres:
        data.update({"genres": genres})
    response = client.post(
        f"{settings.API_V1_STR}/books",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 400, response.text


def test_get_all_books(client: TestClient, admin_auth_header) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/books/all",
        headers=admin_auth_header,
        timeout=8000
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)


def test_get_books(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/books")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)


def test_get_book(client: TestClient, db_book_with_all_attributes: models.Book) -> None:
    book_id = db_book_with_all_attributes.id
    db_book = schemas.Book(
        **vars(db_book_with_all_attributes),
        authors=db_book_with_all_attributes.authors,
        genres=db_book_with_all_attributes.genres,
        image=db_book_with_all_attributes.image,
        pdf=db_book_with_all_attributes.pdf,
        short_pdf=db_book_with_all_attributes.short_pdf
    )
    response = client.get(f"{settings.API_V1_STR}/books/{book_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert db_book.title == data["title"]
    assert db_book.description == data["description"]
    assert db_book.language == data["language"]
    assert db_book.price == data["price"]
    assert db_book.publication_date.strftime("%Y-%m-%d") == data["publication_date"]
    assert db_book.isbn == data["isbn"]
    assert jsonable_encoder(db_book.authors) == data["authors"]
    assert jsonable_encoder(db_book.genres) == data["genres"]
    assert jsonable_encoder(db_book.image) == data["image"]
    assert jsonable_encoder(db_book.pdf) == data["pdf"]
    assert jsonable_encoder(db_book.short_pdf) == data["short_pdf"]


def test_get_book_not_found(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/books/100")
    assert response.status_code == 404, response.text


@pytest.mark.parametrize(
    "field, value",
    [
        ("title", "test upload title"),
        ("description", "test upload description"),
        ("language", "Polish"),
        ("price", 9.99),
        ("publication_date", "2012-12-12"),
        ("isbn", "5315323531311"),
        ("authors", [{"fullname": "test upload author"}]),
        ("genres", [{"name": "test upload genre"}]),
    ]
)
def test_update_book(client: TestClient, admin_auth_header: dict[str, str], field, value) -> None:
    data = {field: value}
    response = client.patch(
        f"{settings.API_V1_STR}/books/1",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 200, response.text
    response_data = response.json()
    if field == "authors":
        assert value[0]["fullname"] == response_data[field][0]["fullname"].lower()
    elif field == "genres":
        assert value[0]["name"] == response_data[field][0]["name"]
    else:
        assert value == response_data[field]


def test_update_book_at_last_param_requirement(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {}
    response = client.patch(
        f"{settings.API_V1_STR}/books/1",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 422, response.text


@pytest.mark.parametrize(
    "authors, genres",
    [
        ([{"fullname": "test first author"}, {"fullname": "test first author"}], None),
        (None, [{"name": "test first genre"}, {"name": "test first genre"}]),
        (
            [{"fullname": "test first author"}, {"fullname": "test first author"}],
            [{"name": "test first genre"}, {"name": "test first genre"}]
        ),
    ]
)
def test_update_book_duplicate_params(client: TestClient, admin_auth_header: dict[str, str], authors, genres) -> None:
    data = {"authors": authors, "genres": genres}
    response = client.patch(
        f"{settings.API_V1_STR}/books/1",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 400, response.text


def test_upload_book_image(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    files = {"image": ("1.jpg", open(IMAGE_PATH_1, "rb"), "image/jpeg")}
    response = client.post(
        f"{settings.API_V1_STR}/books/1/images",
        headers=admin_auth_header,
        files=files
    )
    assert response.status_code == 201, response.content
    assert response.headers["Content-Type"] == "image/jpeg"
    assert "inline;" in response.headers["Content-Disposition"]


def test_upload_book_image_already_exists(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    files = {"image": ("1.jpg", open(IMAGE_PATH_1, "rb"), "image/jpeg")}
    response = client.post(
        f"{settings.API_V1_STR}/books/1/images",
        headers=admin_auth_header,
        files=files
    )
    assert response.status_code == 404, response.text


def test_upload_book_new_image(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    files = {"image": ("2.jpg", open(IMAGE_PATH_2, "rb"), "image/jpeg")}
    response = client.put(
        f"{settings.API_V1_STR}/books/1/images",
        headers=admin_auth_header,
        files=files
    )
    assert response.status_code == 200, response.content
    assert response.headers["Content-Type"] == "image/jpeg"
    assert "inline;" in response.headers["Content-Disposition"]


def test_upload_book_new_image_not_exists(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    files = {"image": ("2.jpg", open(IMAGE_PATH_2, "rb"), "image/jpeg")}
    response = client.put(
        f"{settings.API_V1_STR}/books/2/images",
        headers=admin_auth_header,
        files=files
    )
    assert response.status_code == 404, response.text


def test_get_book_image(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/books/1/images")
    assert response.status_code == 200, response.content
    assert response.headers["Content-Type"] == "image/jpeg"
    assert "inline;" in response.headers["Content-Disposition"]


def test_get_book_image_not_exists(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/books/2/images")
    assert response.status_code == 404, response.text


def test_delete_book_image(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/books/1/images",
        headers=admin_auth_header
    )
    assert response.status_code == 200, response.text


def test_delete_book_image_not_exists(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/books/1/images",
        headers=admin_auth_header
    )
    assert response.status_code == 404, response.text


def test_upload_book_pdf(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    files = {"file": ("Lorem ipsum.pdf", open(PDF_FILE_PATH, "rb"), "application/pdf")}
    response = client.post(
        f"{settings.API_V1_STR}/books/1/pdf",
        headers=admin_auth_header,
        files=files
    )
    assert response.status_code == 201, response.text


def test_upload_book_pdf_already_exists(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    files = {"file": ("Lorem ipsum.pdf", open(PDF_FILE_PATH, "rb"), "application/pdf")}
    response = client.post(
        f"{settings.API_V1_STR}/books/1/pdf",
        headers=admin_auth_header,
        files=files
    )
    assert response.status_code == 400, response.text


# TODO: the header must point to the owner
def test_download_book_pdf(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/books/1/pdf",
        headers=admin_auth_header
    )
    assert response.status_code == 200, response.content
    assert response.headers["Content-Type"] == "application/pdf"


# TODO: the header must point to the owner
def test_download_book_pdf_not_exists(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/books/2/pdf",
        headers=admin_auth_header
    )
    assert response.status_code == 404, response.text


def test_delete_book_pdf(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/books/1/pdf",
        headers=admin_auth_header
    )
    assert response.status_code == 200, response.text


def test_delete_book_pdf_not_exists(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/books/1/pdf",
        headers=admin_auth_header
    )
    assert response.status_code == 404, response.text


def test_upload_book_short_pdf(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    files = {"file": ("Lorem ipsum short.pdf", open(SHORT_PDF_FILE_PATH, "rb"), "application/pdf")}
    response = client.post(
        f"{settings.API_V1_STR}/books/1/short_pdf",
        headers=admin_auth_header,
        files=files
    )
    assert response.status_code == 201, response.text


def test_upload_book_short_pdf_already_exist(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    files = {"file": ("Lorem ipsum short.pdf", open(SHORT_PDF_FILE_PATH, "rb"), "application/pdf")}
    response = client.post(
        f"{settings.API_V1_STR}/books/1/short_pdf",
        headers=admin_auth_header,
        files=files
    )
    assert response.status_code == 400, response.text


def test_download_book_short_pdf(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/books/1/short_pdf")
    assert response.status_code == 200, response.content
    assert response.headers["Content-Type"] == "application/pdf"


def test_download_book_short_pdf_not_exists(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/books/2/short_pdf")
    assert response.status_code == 404, response.text


def test_delete_book_short_pdf(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/books/1/short_pdf",
        headers=admin_auth_header
    )
    assert response.status_code == 200, response.text


def test_delete_book_short_pdf_not_exists(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/books/1/short_pdf",
        headers=admin_auth_header
    )
    assert response.status_code == 404, response.text


def test_get_book_reviews(client: TestClient) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/books/1/reviews"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)


# TODO: the header must point to the owner
def test_create_book_reviews(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "comment": "Great!",
        "rating": 5
    }
    response = client.post(
        f"{settings.API_V1_STR}/books/1/reviews",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 201, response.text


# TODO: the header must point to the owner
def test_create_book_reviews_already_review(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "comment": "Great!",
        "rating": 3
    }
    response = client.post(
        f"{settings.API_V1_STR}/books/1/reviews",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 201, response.text


# TODO: the header must point to the owner
def test_create_book_reviews_invalid_data(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    data = {
        "comment": "Great!",
        "rating": 6
    }
    response = client.post(
        f"{settings.API_V1_STR}/books/1/reviews",
        headers=admin_auth_header,
        json=data
    )
    assert response.status_code == 422, response.text


def test_add_to_wishlist(client: TestClient, user_auth_header: dict[str, str]) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/books/1/wishlist",
        headers=user_auth_header
    )
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    assert isinstance(data, dict)
    assert data["books"][0]["title"] == "test upload title"


def test_delete_book(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    files = {"image": ("2.jpg", open(IMAGE_PATH_2, "rb"), "image/jpeg")}
    client.put(
        f"{settings.API_V1_STR}/books/3/images",
        headers=admin_auth_header,
        files=files
    )
    files = {"file": ("Lorem ipsum.pdf", open(PDF_FILE_PATH, "rb"), "application/pdf")}
    client.post(
        f"{settings.API_V1_STR}/books/3/pdf",
        headers=admin_auth_header,
        files=files
    )
    files = {"file": ("Lorem ipsum short.pdf", open(SHORT_PDF_FILE_PATH, "rb"), "application/pdf")}
    client.post(
        f"{settings.API_V1_STR}/books/3/short_pdf",
        headers=admin_auth_header,
        files=files
    )
    response = client.delete(
        f"{settings.API_V1_STR}/books/3",
        headers=admin_auth_header
    )
    assert response.status_code == 200, response.text
