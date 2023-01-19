from typing import Optional

from app.crud.base import CRUDBase
from app.models.book_image import BookImage
from app.schemas.file import FileCreate, FileUpdate
from pydantic.types import UUID4
from sqlalchemy.orm import Session


class CRUDBookImage(CRUDBase[BookImage, FileCreate, FileUpdate]):
    pass
    # def get_by_book_id(self, db: Session, *, book_id: UUID4) -> BookImage:
    #     return db.query(self.model).filter(self.model.book_id == book_id).first()


book_image = CRUDBookImage(BookImage)
