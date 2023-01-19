from app.db.base_class import Base
from app.models.book_author import book_author
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Author(Base):
    """
    Database model for author of books
    """

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True, unique=True)

    books = relationship("Book", secondary=book_author, back_populates="authors")
