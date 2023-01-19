from typing import Optional

from app.crud.base import CRUDBase
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate
from sqlalchemy.orm import Session


class CRUDGenre(CRUDBase[Genre, GenreCreate, GenreUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Genre]:
        return db.query(self.model).filter(self.model.name == name.lower()).first()

    def create_if_not_exists(self, db: Session, *, obj_in: [GenreCreate, Genre]) -> Genre:
        db_genre = self.get_by_name(db, name=obj_in.name)

        if not db_genre:
            db_genre = self.create(db, obj_in=obj_in)

        return db_genre


genre = CRUDGenre(Genre)