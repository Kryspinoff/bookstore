from typing import Any

from app import crud, schemas
from app.api import deps
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)


@router.post(
    path="",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(deps.require_admin)]
)
async def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_author = crud.author.get_by_fullname(db, fullname=author.fullname)
    if db_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author already exists"
        )
    return crud.author.create(db, obj_in=author)


@router.get(
    path="",
    response_model=list[schemas.Author],
    status_code=status.HTTP_200_OK,
)
async def read_authors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    return crud.author.get_multi(db, skip=skip, limit=limit)


@router.get(
    path="/{author_id}",
    response_model=schemas.Author,
    status_code=status.HTTP_200_OK
)
async def read_author(
    author_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_author = crud.author.get(db, id=author_id)
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return db_author


@router.put(
    path="/{author_id}",
    response_model=schemas.Author,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]
)
async def update_author(
    author_id: int,
    author: schemas.AuthorUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_author = crud.author.get(db, id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The author doesn't exist"
        )
    return crud.author.update(db, db_obj=db_author, obj_in=author)


@router.delete(
    path="/{author_id}",
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]
)
async def delete_author(
    author_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    author = crud.author.get(db, id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    crud.author.remove(db, db_obj=author)
    return schemas.Msg(
        message="Successfully deleted author"
    )


@router.get(
    path="/{author_id}/books",
    response_model=list[schemas.Book],
    status_code=status.HTTP_200_OK,
)
def read_author_books(
    author_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_author = crud.author.get(db, id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author.books
