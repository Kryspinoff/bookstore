from datetime import datetime
from typing import Optional

from app.schemas.base import UpdateValidator
from app.schemas.book import Book
from app.schemas.wishlist import Wishlist
from pydantic import Field, UUID4, BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    first_name: Optional[str] = Field(min_length=3, max_length=32, example="Jan", regex=r"^([a-zA-ZąćęłńóśżźĄĆŁŃÓŚŻŹ](\s?))*([a-zA-ZąćęłńóśżźĄĆŁŃÓŚŻŹ]){1}$")
    last_name: Optional[str] = Field(min_length=3, max_length=32, example="Kowalski", regex=r"^([a-zA-ZąćęłńóśżźĄĆŁŃÓŚŻŹ](\s?|-?))*([a-zA-ZąćęłńóśżźĄĆŁŃÓŚŻŹ]){1}$")
    username: Optional[str] = Field(min_length=6, max_length=32, example="jankowalski", regex=r"^([a-zA-Z0-9](_?))*([a-zA-Z0-9]){1}$")
    email: Optional[EmailStr] = Field(example="jankowalski@example.com")
    phone_number: Optional[str] = Field(min_length=11, max_length=13, example="48500100100")


# Properties to receive via API on creation
class UserCreate(UserBase):
    first_name: str = Field(min_length=3, max_length=32, example="Jan")
    last_name: str = Field(min_length=3, max_length=32, example="Kowalski")
    username: str = Field(min_length=6, max_length=32, example="jankowalski")
    email: EmailStr = Field(example="jankowalski@example.com")
    password: str = Field(min_length=8, max_length=64, example="Password!@#123", regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")


# Properties to create record in DB
class UserCreateInDB(UserCreate):
    role: str
    is_active: Optional[bool] = None


# Properties to receive via API on update
class UserUpdate(UserBase, UpdateValidator):
    pass


class UserInDBBase(UserBase):
    id: UUID4
    role: str
    created_at: datetime
    updated_at: datetime
    wishlist: Optional[Wishlist]

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    is_active: bool
    hashed_password: str
    books: list[Book]
