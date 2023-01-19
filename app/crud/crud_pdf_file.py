from typing import Optional

from app.crud.base import CRUDBase
from app.models.pdf_file import PDFFile
from app.schemas.file import FileCreate, FileUpdate
from pydantic.types import UUID4
from sqlalchemy.orm import Session


class CRUDPDFFile(CRUDBase[PDFFile, FileCreate, FileUpdate]):
    pass
    # def get_by_book_id(self, db: Session, *, book_id: UUID4) -> PDFFile:
    #     return db.query(self.model).filter(self.model.book_id == book_id).first()


pdf_file = CRUDPDFFile(PDFFile)
