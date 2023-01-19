from datetime import timedelta
from typing import Any

from app import crud, schemas
from app.api import deps
from app.constants import Role
from app.core.config import settings
from app.core.security import create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/register",
    tags=["register"]
)


@router.post(
    path="",
    response_model=schemas.Token,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create new user.
    """
    if crud.user.get_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system"
        )
    if crud.user.get_by_username(db, username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists in the system"
        )
    user_in = jsonable_encoder(user_in)
    user_in = schemas.UserCreateInDB(**user_in, role=Role.USER)
    user = crud.user.create(db, obj_in=user_in)

    # Login user when registered
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return schemas.Token(
        access_token=create_access_token(
            user=user,
            expires_delta=access_token_expires
        ),
        token_type="bearer"
    )
