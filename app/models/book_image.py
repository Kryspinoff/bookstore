from datetime import date
from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Column, Date, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class BookImage(Base):
    """
    Database model for image book
    """

    __tablename__ = "book_images"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    filename = Column(String)
    content_type = Column(String)
    upload = Column(Date, default=date.today, onupdate=date.today)

    book_id = Column(Integer, ForeignKey("books.id"), index=True)
    book = relationship("Book", back_populates="image")
