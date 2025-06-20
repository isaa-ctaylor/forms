from operator import is_

import models
import schemas
from sqlalchemy.orm import Session

from .utils import hash_password


def get_user(db: Session, user_id: int):
    return db.query(models.user.User).filter(models.user.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return (
        db.query(models.user.User)
        .filter(models.user.User.is_deleted == False)
        .filter(models.user.User.email == email)
        .first()
    )


def get_user_by_uuid(db: Session, uuid: str):
    return db.query(models.user.User).filter(models.user.User.uuid == uuid).first()


def get_user_by_member_id(db: Session, member_id: str):
    return (
        db.query(models.user.User)
        .filter(models.user.User.details["member_id"].astext == member_id)
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.user.User)
        .filter(models.user.User.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_users_by_role(db: Session, role: str):
    return (
        db.query(models.user.User)
        .filter(models.user.User.is_deleted == False)
        .filter(models.user.User.role == role)
        .all()
    )


def create_user(db: Session, user: schemas.user.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.user.User(
        email=user.email,
        hashed_password=hashed_password,
        details=user.details,
        role=user.role,
        first_name=user.first_name,
        middle_names=user.middle_names,
        last_name=user.last_name,
        is_active=user.is_active,
        is_deleted=user.is_deleted,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, uuid: str, user_update: schemas.user.UserUpdate):
    db_user = db.query(models.user.User).filter(models.user.User.uuid == uuid).first()
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, uuid: str):
    db_user = db.query(models.user.User).filter(models.user.User.uuid == uuid).first()
    if db_user:
        new_db_user = schemas.user.UserUpdate(
            email=db_user.email,  # type: ignore
            is_active=False,
            is_deleted=True,
        )
        db_user = update_user(db, uuid, new_db_user)
        return db_user
    return None
