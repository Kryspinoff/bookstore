from app import crud, schemas
from app.constants import Role
from app.core.config import settings
from sqlalchemy.orm import Session


def init_db(db: Session) -> None:
    # Create Super Admin
    super_admin = crud.user.get_by_username(db, username=settings.FIRST_SUPER_ADMIN_USERNAME)
    if not super_admin:
        super_admin_in = schemas.UserCreateInDB(
            first_name=settings.FIRST_SUPER_ADMIN_FIRST_NAME,
            last_name=settings.FIRST_SUPER_ADMIN_LAST_NAME,
            username=settings.FIRST_SUPER_ADMIN_USERNAME,
            email=settings.FIRST_SUPER_ADMIN_EMAIL,
            password=settings.FIRST_SUPER_ADMIN_PASSWORD,
            role=Role.SUPER_ADMIN
        )
        crud.user.create(db, obj_in=super_admin_in)
