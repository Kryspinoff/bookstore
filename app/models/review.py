from datetime import datetime

from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Review(Base):
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, index=True)
    comment = Column(String, index=True)
    edited = Column(Boolean, default=False, index=True)
    review_date = Column(Date, default=datetime.today, index=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="reviews")

    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="reviews")