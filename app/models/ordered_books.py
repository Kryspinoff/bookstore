from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Table


ordered_books = Table(
    "ordered_books",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id")),
    Column("book_id", ForeignKey("books.id")),
)