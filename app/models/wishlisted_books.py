from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint, Table


wishlisted_books = Table(
    "wishlisted_books",
    Base.metadata,
    Column("wishlist_id", ForeignKey("wishlists.id")),
    Column("book_id", ForeignKey("books.id")),
)
