from datetime import date
from typing import Optional

from app.schemas.author import Author, AuthorCreate
from app.schemas.file import File
from app.schemas.genre import Genre, GenreCreate
from app.schemas.base import UpdateValidator
from pydantic import BaseModel, Field
from fastapi import Body


# Shared properties
class BookBase(BaseModel):
    title: Optional[str] = Field(
        min_length=1,
        max_length=128,
        example="Think again: the power of knowing what you don't know"
    )
    description: Optional[str] = Field(
        example="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
                "do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    )
    language: Optional[str] = Field(
        example="Polish"
    )
    price: Optional[float] = Field(example=0)
    publication_date: Optional[date] = Field(example="2019-09-11")
    isbn: Optional[str] = Field(
        min_length=13,
        max_length=13,
        regex=r"^([0-9]{13})$",
        example="9780593395783"
    )
    authors: list[AuthorCreate] = Body(None)
    genres: list[GenreCreate] = Body(None)


# Properties to receive via API on creation
class BookCreate(BookBase):
    title: str = Field(
        min_length=1,
        max_length=128,
        example="Think again: the power of knowing what you don't know"
    )
    language: str = Field(
        example="Polish"
    )
    price: float = Field(default=0, example=0)
    publication_date: date = Field(example="2019-09-11")


# Properties to receive via API on update
class BookUpdate(BookBase, UpdateValidator):
    pass


class BookInDBBase(BookBase):
    id: int
    avg_rating: Optional[float]
    authors: Optional[list[Author]]
    genres: Optional[list[Genre]]
    image: Optional[File]
    pdf: Optional[File]
    short_pdf: Optional[File]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Book(BookInDBBase):
    pass


class BookInDB(BookInDBBase):
    pass
