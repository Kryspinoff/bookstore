from app.schemas.book import Book
from pydantic import BaseModel


class Wishlist(BaseModel):
    id: int
    books: list[Book]

    class Config:
        orm_mode = True

