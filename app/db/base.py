# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.models.author import Author
from app.models.book import Book
from app.models.book_author import book_author
from app.models.book_genre import book_genre
from app.models.book_ownership import book_ownership
from app.models.genre import Genre
from app.models.book_image import Base
from app.models.order import Order
from app.models.ordered_books import ordered_books
from app.models.pdf_file import PDFFile
from app.models.review import Review
from app.models.short_pdf_file import ShortPDFFile
from app.models.user import User
from app.models.wishlist import Wishlist
from app.models.wishlisted_books import wishlisted_books
