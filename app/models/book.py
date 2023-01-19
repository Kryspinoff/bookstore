from app.db.base_class import Base
from app.models.review import Review
from app.models.book_genre import book_genre
from app.models.book_author import book_author
from app.models.book_ownership import book_ownership
from app.models.ordered_books import ordered_books
from app.models.wishlisted_books import wishlisted_books
from sqlalchemy import Column, Date, Float, Integer, String, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy_utils import aggregated


class Book(Base):
    """
    Database model for book
    """

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False, index=True)
    description = Column(Text, index=True)
    language = Column(String, index=True)
    publication_date = Column(Date, index=True)
    price = Column(Float, nullable=False, index=True)
    isbn = Column(String(13), index=True)

    # https://sqlalchemy-utils.readthedocs.io/en/latest/aggregates.html#average-movie-rating
    @aggregated("reviews", Column(Float))
    def avg_rating(self) -> float:
        return func.avg(Review.rating)

    reviews = relationship("Review", back_populates="book")

    image = relationship("BookImage", back_populates="book", uselist=False)

    pdf = relationship("PDFFile", back_populates="book", uselist=False)

    short_pdf = relationship("ShortPDFFile", back_populates="book", uselist=False)

    authors = relationship("Author", secondary=book_author, back_populates="books")

    genres = relationship("Genre", secondary=book_genre, back_populates="books")

    owners = relationship("User", secondary=book_ownership, back_populates="books")

    orders = relationship("Order", secondary=ordered_books, back_populates="ordered_books")

    wishlists = relationship("Wishlist", secondary=wishlisted_books, back_populates="books")

    __mapper_args__ = {"eager_defaults": True}
