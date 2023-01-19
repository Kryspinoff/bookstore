from typing import Optional

from app.crud.base import CRUDBase
from app.models.short_pdf_file import ShortPDFFile
from app.schemas.file import FileCreate, FileUpdate
from pydantic.types import UUID4
from sqlalchemy.orm import Session


class CRUDShortPDFFile(CRUDBase[ShortPDFFile, FileCreate, FileUpdate]):
    pass
    # def get_by_book_id(self, db: Session, *, book_id: UUID4) -> ShortPDFFile:
    #     return db.query(self.model).filter(self.model.book_id == book_id).first()


short_pdf_file = CRUDShortPDFFile(ShortPDFFile)
