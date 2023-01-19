from typing import Any

from app import crud, schemas
from app.api import deps
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(deps.require_admin)]
)


@router.get(
    path="",
    response_model=list[schemas.Order],
    status_code=status.HTTP_200_OK
)
def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve all orders.
    """
    return crud.order.get_multi(db, skip=skip, limit=limit)
