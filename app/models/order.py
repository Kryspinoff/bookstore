from app.db.base_class import Base
from app.models.ordered_books import ordered_books
from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date, index=True)
    total_price = Column(Float, index=True)
    order_id = Column(String, index=True)
    completed = Column(Boolean, default=False, index=True)

    client_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    client = relationship("User", back_populates="orders")

    ordered_books = relationship(
        "Book", secondary=ordered_books, back_populates="orders"
    )
