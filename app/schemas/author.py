from app.schemas.base import UpdateValidator
from pydantic import BaseModel, Field, validator


# Shared properties
class AuthorBase(BaseModel):
    fullname: str = Field(
        min_length=6,
        max_length=32,
        regex=r"^([a-zA-ZąćęłńóśżźĄĆŁŃÓŚŻŹ]([.]?\s?|-?))*([a-zA-ZąćęłńóśżźĄĆŁŃÓŚŻŹ]){1}$",
        example="Stephen Edwin King"
    )

    @validator("fullname")
    def valid_fullname(cls, value: str):
        return value.title()

    def __hash__(self):
        return hash(tuple(self))

    def __repr__(self):
        return self.fullname


# Properties to receive via API on creation
class AuthorCreate(AuthorBase):
    pass


# Properties to receive via API on update
class AuthorUpdate(AuthorBase, UpdateValidator):
    pass


class AuthorInDBBase(AuthorBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Author(AuthorInDBBase):
    pass


# Additional properties to return via API
class AuthorInDB(AuthorInDBBase):
    pass
