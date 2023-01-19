from typing import Any

from app import crud, schemas
from app.api import deps
from app.core import security
from app.schemas.token import Token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/login",
    tags=["login"]
)


@router.post(
    path="",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK
)
def login_user(
    db: Session = Depends(deps.get_db),
    from_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    if "@" in from_data.username:
        user = crud.user.authenticate(db, email=from_data.username, password=from_data.password)
    else:
        user = crud.user.authenticate(db, username=from_data.username, password=from_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username/email or password"
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return Token(
        access_token=security.create_access_token(
            user=user
        ),
        token_type="Bearer"
    )