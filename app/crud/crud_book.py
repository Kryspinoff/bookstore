from typing import Optional

from app.crud.base import CRUDBase
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload


class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    def get_by_title(self, db: Session, *, title: str) -> Optional[Book]:
        return db.query(self.model).filter(self.model.title == title).first()

    async def get_all_books(self, db: AsyncSession) -> list[Book]:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.authors))
            .options(joinedload(self.model.genres))
            .options(joinedload(self.model.image))
            .options(joinedload(self.model.pdf))
            .options(joinedload(self.model.short_pdf))
        )
        result = await db.execute(stmt)
        return [db_book for db_book in result.unique().scalars()]


book = CRUDBook(Book)
