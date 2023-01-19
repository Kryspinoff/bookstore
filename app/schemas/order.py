from datetime import datetime, date
from typing import Optional, TypeVar, Dict

from app.schemas.user import User
from app.schemas.book import Book
from app.schemas.base import UpdateValidator
from pydantic import UUID4, BaseModel, Field


# Shared properties
class OrderBase(BaseModel):
    order_date: Optional[date] = Field(example="15.04.2019")
    total_price: Optional[float] = Field(example=0)
    order_id: Optional[str]
    completed: Optional[bool]


# Properties to receive via API on creation
class OrderCreate(OrderBase):
    order_date: date = Field(example="15.04.2019")
    total_price: float = Field(example=0)
    order_id: str
    completed: bool


# Properties to receive via API on update
class OrderUpdate(OrderBase, UpdateValidator):
    pass


class OrderInDBBase(OrderBase):
    id: UUID4
    client: Optional[User]
    ordered_books: list[Book]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Order(OrderInDBBase):
    pass


class OrderInDB(OrderInDBBase):
    pass
