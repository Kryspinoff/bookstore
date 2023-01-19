from typing import Any

from app import crud, schemas
from app.api import deps
from app.constants.role import Role
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr, UUID4
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(deps.require_admin)]
)


@router.get(
    path="",
    response_model=list[schemas.User],
    status_code=status.HTTP_200_OK,
)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve all users.
    """
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.get(
    path="/{user_id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
)
async def read_user(
    user_id: UUID4,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.patch(
    path="/{user_id}/set_role",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(deps.require_superadmin)]
)
async def set_role(
    user_id: UUID4,
    role: Role,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Update a role for user
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist in database"
        )
    user = crud.user.update(db, db_obj=user, obj_in={"role": role})
    return user
