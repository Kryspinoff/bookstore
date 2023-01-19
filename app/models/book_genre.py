from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Table


book_genre = Table(
    "book_genres",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)
