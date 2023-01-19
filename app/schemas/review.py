from datetime import date

from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    rating: int = Field(ge=0, le=5)
    comment: str


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    pass


class ReviewInDBBase(ReviewBase):
    id: int
    edited: bool
    review_date: date

    class Config:
        orm_mode = True


class Review(ReviewInDBBase):
    pass


class ReviewInDB(ReviewInDBBase):
    pass
