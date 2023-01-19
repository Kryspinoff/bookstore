from app.db.base_class import Base
from app.models.book_genre import book_genre
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Genre(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)

    books = relationship("Book", secondary=book_genre, back_populates="genres")
