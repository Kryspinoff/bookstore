from typing import Any

from app import crud, schemas
from app.api import deps
from app.constants import Role
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)


@router.put(
    path="/{review_id}",
    response_model=schemas.Review,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.get_current_user)]
)
async def update_review(
    review_id: int,
    updated_review: schemas.ReviewUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_review = crud.review.get(db, id=review_id)
    if not db_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    return crud.review.update(db, db_obj=db_review, obj_in=updated_review)


@router.delete(
    path="/{review_id}",
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK
)
async def delete_review(
    review_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    db_review = crud.review.get(db, id=review_id)
    if not db_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if not db_review.user == current_user and current_user.role not in [Role.ADMIN, Role.SUPER_ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    crud.review.remove(db, db_obj=db_review)
    return schemas.Msg(
        message="Successful delete review"
    )
