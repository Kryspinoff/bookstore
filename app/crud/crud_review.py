from typing import Optional

from app import models
from app.crud.base import CRUDBase
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
from sqlalchemy.orm import Session
from pydantic import UUID4


class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):
    def get_by_user(self, db: Session, *, user: models.User, book_id: int) -> Optional[Review]:
        return (
            db.query(self.model)
            .filter(self.model.user == user, self.model.book_id == book_id)
            .first()
        )

    def update(self, db: Session, *, db_obj: models.Review, obj_in: ReviewCreate) -> Review:
        db_obj.edited = True
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


review = CRUDReview(Review)
