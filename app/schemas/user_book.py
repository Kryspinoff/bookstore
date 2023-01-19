from datetime import datetime
from typing import Optional

from app.schemas.book import Book
from app.schemas.user import User
from pydantic import UUID4, BaseModel


# Shared properties
class UserBookBase(BaseModel):
    user_id: Optional[UUID4]
    book_id: Optional[UUID4]


# Properties to receive via API on creation
class UserBookCreate(UserBookBase):
    pass


# Properties to receive via API on update
class UserBookUpdate(UserBookBase):
    pass


class UserBookInDBBase(UserBookBase):
    date_of_borrowing: datetime
    user: User
    book: Book

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserBook(UserBookInDBBase):
    pass


class UserBookInDB(UserBookInDBBase):
    pass
