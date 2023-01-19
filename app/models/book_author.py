from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Table


book_author = Table(
    "book_authors",
    Base.metadata,
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)
