from app.crud.base import CRUDBase
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate
from sqlalchemy.orm import Session


class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    def get_by_fullname(self, db: Session, *, fullname: str) -> Author:
        return db.query(self.model).filter(self.model.fullname == fullname).first()

    def create_if_not_exists(self, db: Session, *, obj_in: [AuthorCreate, Author]) -> Author:
        db_author = self.get_by_fullname(db, fullname=obj_in.fullname)

        if not db_author:
            db_author = self.create(db, obj_in=obj_in)

        return db_author


author = CRUDAuthor(Author)
