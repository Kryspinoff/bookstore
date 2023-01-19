from datetime import datetime
from uuid import uuid4

from app.db.base_class import Base
from app.models.book_ownership import book_ownership
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    """
    Database model for an application user
    """

    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    username = Column(String(32), unique=True, index=True, nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    phone_number = Column(String(13), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    role = Column(String(32), unique=False, index=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    orders = relationship("Order", back_populates="client")

    books = relationship("Book", secondary=book_ownership, back_populates="owners")

    reviews = relationship("Review", back_populates="user")
    
    wishlist = relationship("Wishlist", back_populates="user", uselist=False)
