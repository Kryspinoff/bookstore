from app.db.base_class import Base
from app.models.wishlisted_books import wishlisted_books
from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class Wishlist(Base):
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="wishlist")

    books = relationship("Book", secondary=wishlisted_books, back_populates="wishlists")