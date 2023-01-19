from typing import Any, Optional

from app import crud, models, schemas
from app.api import deps
from app.core.security import verify_password
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)


@router.get(
    path="",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
def get_profile(
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve current use.
    """
    return current_user


@router.get(
    path="/library",
    response_model=list[schemas.Book],
    status_code=status.HTTP_200_OK
)
def get_user_library(
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve owner books for current user.
    """
    return current_user.books


@router.get(
    path="/wishlist",
    response_model=Optional[schemas.Wishlist],
    status_code=status.HTTP_200_OK
)
def get_user_wishlist(
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve wishlist for current user.
    """
    return current_user.wishlist


@router.patch(
    path="",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
def update_profile(
    user_in: schemas.UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Update current user.
    """
    if (
        user_in.email is not None
        and crud.user.get_by_email(db, email=user_in.email)
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The email is already used"
        )
    if (
        user_in.username is not None
        and crud.user.get_by_username(db, username=user_in.username)
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The username is already used"
        )
    return crud.user.update(db, db_obj=current_user, obj_in=user_in)


@router.patch(
    path="/set_new_password",
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK
)
async def set_new_password(
    password: str = Body(
        min_length=8,
        max_length=64,
        example="Password!@#123",
        regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    ),
    new_password: str = Body(
        min_length=8,
        max_length=64,
        example="Password!@#123",
        regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    ),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Update password for current user.
    """
    if not verify_password(password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have entered the wrong password"
        )
    if verify_password(new_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have entered an existing new password"
        )
    crud.user.update(db, db_obj=current_user, obj_in={"password": new_password})
    return schemas.Msg(
        message="Successful change password"
    )


@router.delete(
    path="",
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK
)
async def delete_profile(
    password: str = Query(
        min_length=8,
        max_length=64,
        example="Password!@#123",
        regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    ),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Delete owner profile.
    """
    if not verify_password(password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have entered the wrong password"
        )
    crud.user.remove(db, db_obj=current_user)
    return schemas.Msg(
        message="Successful delete profile."
    )
