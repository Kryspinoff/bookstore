from typing import Any

from app import schemas
from app.api import deps
from app.db.session import engine
from app.db.base_class import Base
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix="/dev",
    tags=["dev"]
)


@router.get(
    path="/super_admin_required",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
async def super_admin_required(
    current_user: schemas.User = Depends(deps.require_superadmin)
) -> Any:
    return current_user


@router.get(
    path="/admin_required",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
async def admin_required(
    current_user: schemas.User = Depends(deps.require_admin)
) -> Any:
    return current_user


# Require authentication
@router.get(
    path="/auth_required",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
async def auth_required(
    current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    return current_user


@router.get(
    path="/auth_optional",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
async def auth_optional(
    current_user: schemas.User = Depends(deps.get_current_user_or_none)
) -> Any:
    return current_user


@router.get(
    path="/drop_tables",
    response_model=schemas.Msg,
    dependencies=[Depends(deps.require_superadmin)],
    status_code=status.HTTP_200_OK
)
async def drop_tables() -> Any:
    Base.metadata.drop_all(bind=engine, checkfirst=True)
    return schemas.Msg(
        message="Drop tables"
    )


@router.get(
    path="/create_tables",
    response_model=schemas.Msg,
    dependencies=[Depends(deps.require_superadmin)],
    status_code=status.HTTP_200_OK
)
async def create_tables() -> Any:
    Base.metadata.create_all(bind=engine, checkfirst=True)
    return schemas.Msg(
        message="Create tables"
    )
