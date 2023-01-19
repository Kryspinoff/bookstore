# from typing import Optional
#
# from app.crud.base import CRUDBase
# from app.models.book_author import book_author
# from app.schemas.book_author import BookAuthorCreate, BookAuthorUpdate
# from pydantic.types import UUID4
# from sqlalchemy.orm import Session
#
#
# class CRUDBookAuthor(CRUDBase[book_author, BookAuthorCreate, BookAuthorUpdate]):
#     def get_by_author_id(self, db: Session, *, author_id: UUID4) -> Optional[list[book_author]]:
#         return db.query(self.model).filter(self.model.author_id == author_id).all()
#
#     def get_by_book_id(self, db: Session, *, book_id: UUID4) -> Optional[list[book_author]]:
#         return db.query(self.model).filter(self.model.book_id == book_id).all()
#
#
# book_author = CRUDBookAuthor(book_author)
