from typing import Any, Dict, Optional, Union

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreateInDB, UserUpdate
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreateInDB, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreateInDB) -> User:
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            phone_number=obj_in.phone_number,
            hashed_password=get_password_hash(obj_in.password),
            role=obj_in.role
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: [UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, password: str, email: str = None, username: str = None) -> Optional[User]:
        if email:
            user = self.get_by_email(db, email=email)
        elif username:
            user = self.get_by_username(db, username=username)
        else:
            return None

        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.username == username).first()

    # @staticmethod
    # def set_password(db: Session, *, db_obj: User, password: str) -> User:
    #     db_obj.hashed_password = get_password_hash(password)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj


user = CRUDUser(User)
