import os
from typing import Any, Optional

from app import crud, models, schemas
from app.api import deps
from app.constants.static_file_dir import StaticFile
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.post(
    path="",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(deps.require_admin)]
)
async def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Create new book.
    """
    db_book = crud.book.get_by_title(db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this title already exists"
        )

    if result := duplicate(authors=book.authors, genres=book.genres):
        raise http_duplicate_exception(result)

    db_authors = []
    if book.authors:
        for author in book.authors:
            db_authors.append(
                crud.author.create_if_not_exists(db, obj_in=author)
            )
        del book.authors

    db_genres = []
    if book.genres:
        for genre in book.genres:
            db_genres.append(
                crud.genre.create_if_not_exists(db, obj_in=genre)
            )
        del book.genres

    book_data = jsonable_encoder(book.dict(exclude_unset=True))
    book_in = models.Book(**book_data)
    book_in.genres = db_genres
    book_in.authors = db_authors
    return crud.book.create(db=db, obj_in=book_in)


@router.get(
    path="/all",
    response_model=list[schemas.Book],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]
)
async def read_all_books(
    db: AsyncSession = Depends(deps.get_async_db)
) -> Any:
    return await crud.book.get_all_books(db)


@router.get(
    path="",
    response_model=list[schemas.Book],
    status_code=status.HTTP_200_OK
)
async def read_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve all books.
    """
    books = crud.book.get_multi(db, skip=skip, limit=limit)
    return books


@router.get(
    path="/{book_id}",
    response_model=schemas.Book,
    status_code=status.HTTP_200_OK
)
async def read_book(
    db_book: models.Book = Depends(deps.get_db_book)
):
    """
    Retrieve a book by it's ID.
    """
    return db_book


@router.patch(
    path="/{book_id}",
    response_model=schemas.Book,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]
)
async def update_book(
    book_id: int,
    book_in: Optional[schemas.BookUpdate],
    db: Session = Depends(deps.get_db),
    db_book: models.Book = Depends(deps.get_db_book)
) -> Any:
    """
    Update a book by it's ID.
    """
    if result := duplicate(authors=book_in.authors, genres=book_in.genres):
        raise http_duplicate_exception(result)

    if book_in.authors:
        db_authors = []
        for author_in in book_in.authors:
            db_authors.append(
                crud.author.create_if_not_exists(db, obj_in=author_in)
            )

        db_book.authors = db_authors
        del book_in.authors

    if book_in.genres:
        db_genres = []
        for genre_in in book_in.genres:
            db_genres.append(
                crud.genre.create_if_not_exists(db, obj_in=genre_in)
            )

        db_book.genres = db_genres
        del book_in.genres

    return crud.book.update(db, db_obj=db_book, obj_in=book_in)


@router.delete(
    path="/{book_id}",
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]
)
async def delete_book(
    book_id: int,
    db: Session = Depends(deps.get_db),
    db_book: models.Book = Depends(deps.get_db_book)
) -> Any:
    """
    Remove book.
    """
    if db_book.image:
        images_dir_path = os.path.join(StaticFile.images_books, str(book_id))
        delete_dir_with_content(images_dir_path)
        crud.book_image.remove(db, db_obj=db_book.image)

    files_dir_path = os.path.join(StaticFile.files_books, str(book_id))

    if db_book.pdf:
        crud.pdf_file.remove(db, db_obj=db_book.pdf)

    if db_book.short_pdf:
        crud.short_pdf_file.remove(db, db_obj=db_book.short_pdf)

    if os.path.exists(files_dir_path):
        delete_dir_with_content(files_dir_path)

    crud.book.remove(db, db_obj=db_book)

    return schemas.Msg(
        message="Successful delete book"
    )


@router.post(
    path="/{book_id}/images",
    response_class=FileResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(deps.require_admin)]
)
async def upload_image(
    book_id: int,
    image: UploadFile,
    db: Session = Depends(deps.get_db),
    db_book: models.Book = Depends(deps.get_db_book)
) -> Any:
    """
    Upload image of book.
    """
    if db_book.image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image already exists"
        )

    filename = image.filename
    content_type = image.content_type
    save_dir_path = os.path.join(StaticFile.images_books, str(book_id))
    save_file_path = os.path.join(save_dir_path, filename)

    os.mkdir(save_dir_path)
    await save_file(save_file_path, image)

    image_in = schemas.FileCreate(
        filename=filename,
        content_type=content_type
    )

    db_image = crud.book_image.create(db, obj_in=image_in)
    db_book.image = db_image
    db.add(db_image)
    db.commit()
    db.refresh(db_book)

    dir_path = os.path.join(StaticFile.images_books, str(book_id))
    image_path = os.path.join(dir_path, filename)

    response = FileResponse(
        image_path,
        status_code=201,
        filename=filename,
        media_type=content_type
    )
    response.headers["Content-Disposition"] = f"inline; filename={filename}"
    return response


@router.get(
    path="/{book_id}/images",
    response_class=FileResponse
)
async def get_image(
    book_id: int,
    db_book: models.Book = Depends(deps.get_db_book)
) -> FileResponse:
    """
    Retrieve image of book.
    """
    http_not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    db_image = db_book.image
    if not db_image:
        raise http_not_found_exception

    filename = db_image.filename
    media_type = db_image.content_type
    dir_path = os.path.join(StaticFile.images_books, str(book_id))
    image_path = os.path.join(dir_path, filename)

    if not os.path.exists(image_path):
        raise http_not_found_exception

    response = FileResponse(
        image_path,
        status_code=200,
        filename=filename,
        media_type=media_type
    )
    response.headers["Content-Disposition"] = f"inline; filename={filename}"
    return response


@router.put(
    path="/{book_id}/images",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]
)
async def upload_new_image(
    book_id: int,
    image: UploadFile,
    db: Session = Depends(deps.get_db),
    db_book: models.Book = Depends(deps.get_db_book)
) -> FileResponse:
    """
    Upload new image of book.
    """
    db_image = db_book.image
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    save_dir_path = os.path.join(StaticFile.images_books, str(book_id))
    save_file_path = os.path.join(save_dir_path, image.filename)
    delete_file_path = os.path.join(save_dir_path, db_book.image.filename)

    delete_file(file_path=delete_file_path)
    await save_file(save_file_path, image)

    image_in = schemas.FileCreate(
        filename=image.filename,
        content_type=image.content_type
    )

    db_image = crud.book_image.update(db, db_obj=db_image, obj_in=image_in)
    filename = db_image.filename
    media_type = db_image.content_type
    dir_path = os.path.join(StaticFile.images_books, str(book_id))
    image_path = os.path.join(dir_path, db_image.filename)

    response = FileResponse(
        image_path,
        status_code=200,
        filename=filename,
        media_type=media_type
    )
    response.headers["Content-Disposition"] = f"inline; filename={filename}"
    return response


@router.delete(
    path="/{book_id}/images",
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]
)
async def delete_image(
    book_id: int,
    db: Session = Depends(deps.get_db),
    db_book: models.Book = Depends(deps.get_db_book)
) -> Any:
    """
    Delete image of book.
    """
    if not db_book.image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    dir_path = os.path.join(StaticFile.images_books, str(book_id))

    delete_dir_with_content(dir_path)
    crud.book_image.remove(db, db_obj=db_book.image)

    return schemas.Msg(
        message="Successful delete image"
    )


@router.post(
    path="/{book_id}/pdf",
    response_model=schemas.Msg,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(deps.require_admin)]
)
async def upload_pdf_file(
    book_id: int,
    file: UploadFile,
    db: Session = Depends(deps.get_db),
    db_book: models.Book = Depends(deps.get_db_book)
):
    """
    Upload PDF file of book.
    """
    db_pdf = db_book.pdf
    if db_pdf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF file already exists"
        )
    save_dir_path = os.path.join(StaticFile.files_books, str(book_id))
    save_file_path = os.path.join(save_dir_path, file.filename)

    if not os.path.exists(save_dir_path):
        os.mkdir(save_dir_path)

    await save_file(save_file_path, file)

    file_in = schemas.FileCreate(
        filename=file.filename,
        content_type=file.content_type
    )

    db_pdf = crud.pdf_file.create(db, obj_in=file_in)

    db_book.pdf = db_pdf
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return schemas.Msg(
        message="Successful update pdf file"
    )


@router.get(
    path="/{book_id}/pdf",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]  # TODO: Add depends for owner book
)
async def download_pdf_file(
    book_id: int,
    db_book: models.Book = Depends(deps.get_db_book)
) -> FileResponse:
    """
    Download PDF file of book.
    """
    http_not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF not found"
        )
    db_pdf = db_book.pdf
    if not db_pdf:
        raise http_not_found_exception

    filename = db_pdf.filename
    media_type = db_pdf.content_type
    dir_path = os.path.join(StaticFile.files_books, str(book_id))
    file_path = os.path.join(dir_path, filename)

    if not os.path.exists(file_path):
        raise http_not_found_exception

    return FileResponse(file_path, media_type=media_type, filename=filename)


@router.delete(
    path="/{book_id}/pdf",
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]
)
async def delete_pdf_file(
    book_id: int,
    db: Session = Depends(deps.get_db),
    db_book: models.Book = Depends(deps.get_db_book)
) -> Any:
    """
    Delete PDF file of book.
    """
    db_pdf = db_book.pdf
    if not db_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF not found"
        )

    filename = db_pdf.filename
    dir_path = os.path.join(StaticFile.files_books, str(book_id))
    file_path = os.path.join(dir_path, filename)

    delete_file(file_path=file_path)
    if not os.listdir(dir_path):
        delete_dir_with_content(dir_path)

    crud.pdf_file.remove(db, db_obj=db_pdf)

    return schemas.Msg(
        message="Successful delete image"
    )


@router.post(
    path="/{book_id}/short_pdf",
    response_model=schemas.Msg,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(deps.require_admin)]
)
async def upload_short_pdf_file(
    book_id: int,
    file: UploadFile,
    db: Session = Depends(deps.get_db),
    db_book: models.Book = Depends(deps.get_db_book)
) -> Any:
    """
    Upload short PDF file of book.
    """
    db_short_pdf = db_book.short_pdf
    if db_short_pdf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Short PDF is already exists"
        )

    filename = file.filename
    content_type = file.content_type
    save_dir_path = os.path.join(StaticFile.files_books, str(book_id))
    save_file_path = os.path.join(save_dir_path, filename)

    if not os.path.exists(save_dir_path):
        os.mkdir(save_dir_path)

    await save_file(save_file_path, file)

    file_in = schemas.FileCreate(
        filename=filename,
        content_type=content_type
    )

    db_short_pdf = crud.short_pdf_file.create(db, obj_in=file_in)

    db_book.short_pdf = db_short_pdf
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return schemas.Msg(
        message="Successful update pdf file"
    )


@router.get(
    path="/{book_id}/short_pdf",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK
)
async def download_short_pdf_file(
    book_id: int,
    db_book: models.Book = Depends(deps.get_db_book)
) -> FileResponse:
    """
    Download short PDF file of book.
    """
    http_not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short PDF not found"
        )

    db_short_pdf = db_book.short_pdf
    if not db_short_pdf:
        raise http_not_found_exception

    filename = db_short_pdf.filename
    media_type = db_short_pdf.content_type
    dir_path = os.path.join(StaticFile.files_books, str(book_id))
    file_path = os.path.join(dir_path, filename)

    if not os.path.exists(file_path):
        raise http_not_found_exception

    return FileResponse(file_path, media_type=media_type, filename=filename)


@router.delete(
    path="/{book_id}/short_pdf",
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]
)
async def delete_short_pdf_file(
    book_id: int,
    db: Session = Depends(deps.get_db),
    db_book: models.Book = Depends(deps.get_db_book)
) -> Any:
    """
    Remove short PDF file of book.
    """
    db_short_pdf = db_book.short_pdf
    if not db_short_pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short PDF not found"
        )

    filename = db_short_pdf.filename
    dir_path = os.path.join(StaticFile.files_books, str(book_id))
    file_path = os.path.join(dir_path, filename)

    delete_file(file_path=file_path)
    if not os.listdir(dir_path):
        delete_dir_with_content(dir_path)

    crud.book_image.remove(db, db_obj=db_short_pdf)

    return schemas.Msg(
        message="Successful delete image"
    )


@router.get(
    path="/{book_id}/reviews",
    response_model=list[schemas.Review],
    status_code=status.HTTP_200_OK
)
async def read_reviews(
    db_book: models.Book = Depends(deps.get_db_book)
) -> Any:
    """
    Retrieve all reviews of book.
    """
    return db_book.reviews


@router.post(
    path="/{book_id}/reviews",
    response_model=schemas.Review,
    status_code=status.HTTP_201_CREATED
)
async def review_book(
    book_id: int,
    review: schemas.ReviewCreate,
    current_user: models.User = Depends(deps.get_current_user),  # TODO: Możliwość oceniania książki tylko dla osób które wykupiły wcześniej dostęp
    db: Session = Depends(deps.get_db),
    db_book: models.Book = Depends(deps.get_db_book)
) -> Any:
    db_review = crud.review.get_by_user(db, user=current_user, book_id=book_id)
    if db_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You have already reviewed this book"
        )

    review_in = models.Review(**review.dict(exclude_unset=True))
    review_in.user = current_user
    review_in.book = db_book

    return crud.review.create(db, obj_in=review_in)


@router.get(
    path="/{book_id}/wishlist",
    response_model=schemas.Wishlist,
    status_code=status.HTTP_200_OK
)
async def wishlist_book(
    book_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
    db_book: models.Book = Depends(deps.get_db_book)
) -> Any:
    return crud.toggle.wishlist_book(db, book=db_book, user=current_user)


# Below are additional functions that are part of file handling.
# File features
async def save_file(file_path, file) -> None:
    with open(file_path, 'wb') as out_file:
        while content := await file.read(1024):
            out_file.write(content)


# File features
def delete_dir_with_content(dir_path) -> None:
    try:
        for file in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, file))
        os.rmdir(dir_path)
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="To many requests"
        )


# File features
def delete_file(file_path) -> None:
    try:
        os.remove(file_path)
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="To many requests"
        )


# Checking for duplicates in request params.
def duplicate(**kwargs) -> Optional[dict[str, str]]:
    """
    arg_name: object name
    arg_value: object
    """
    for name_obj, objs in kwargs.items():
        if not isinstance(objs, list):
            continue
        if len(uniq := list(set(objs))) != len(objs):
            return {
                "name": name_obj,
                "objects": objs,
                "uniq": uniq
            }
    return None


# A function that returns an exception for duplicates in request params.
def http_duplicate_exception(info: dict) -> HTTPException:
    name = info.get('name')
    objects = info.get('objects')
    uniq = info.get('uniq')
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Duplicate {name} not allowed. {name}: {objects}, uniq: {uniq}"
    )

