from typing import Any

from app import crud, schemas
from app.api import deps
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/genres",
    tags=["genres"]
)


@router.post(
    path="",
    response_model=schemas.Genre,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(deps.require_admin)]
)
async def create_genre(
    genre: schemas.GenreCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Create new genre.
    """
    db_genre = crud.genre.get_by_name(db, name=genre.name)
    if db_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre with this name already exists"
        )

    return crud.genre.create(db, obj_in=genre)


@router.put(
    path="/{genre_id}",
    response_model=schemas.Genre,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]
)
async def update_genre(
    genre_id: int,
    genre: schemas.GenreUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Update genre.
    """
    db_genre = crud.genre.get(db, id=genre_id)
    if not db_genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The book doesn't exist"
        )

    return crud.genre.update(db, db_obj=db_genre, obj_in=genre)


@router.get(
    path="",
    response_model=list[schemas.Genre],
    status_code=status.HTTP_200_OK
)
async def read_genres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve all genres.
    """
    genres = crud.genre.get_multi(db, skip=skip, limit=limit)
    return genres


@router.get(
    path="/{genre_id}",
    response_model=schemas.Genre,
    status_code=status.HTTP_200_OK
)
async def read_genre(
    genre_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve genres by it's ID.
    """
    db_genre = crud.genre.get(db, id=genre_id)
    if not db_genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genres not found")
    print(db_genre.name)
    print(db_genre.books)
    return db_genre


@router.get(
    path="/{genre_id}/books",
    response_model=list[schemas.Book],
    status_code=status.HTTP_200_OK,
)
def read_genre_books(
    genre_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve books by genre name.
    """
    genre = crud.genre.get(db, id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genres not found")
    return genre.books


@router.delete(
    path="/{genre_id}",
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_admin)]
)
async def delete_genre(
    genre_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Remove genre.
    """
    genre = crud.genre.get(db, id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genres not found")

    crud.genre.remove(db, db_obj=genre)
    return schemas.Msg(
        message="Successful delete genre"
    )