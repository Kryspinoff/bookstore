from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Table


book_ownership = Table(
    "book_ownership",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)
