import models
import schemas
from sqlalchemy.orm import Session

from .utils import generate_member_id, hash_password


def get_user(db: Session, user_id: int):
    return db.query(models.user.User).filter(models.user.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.user.User).filter(models.user.User.email == email).first()


def get_user_by_uuid(db: Session, uuid: str):
    return db.query(models.user.User).filter(models.user.User.uuid == uuid).first()


def get_user_by_member_id(db: Session, member_id: str):
    return (
        db.query(models.user.User)
        .filter(models.user.User.member_id == member_id)
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.user.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.user.UserCreate):
    hashed_password = hash_password(user.password)  # Hash the password
    db_user = models.user.User(
        email=user.email,
        hashed_password=hashed_password,  # Store the hashed password
        member_id=(
            user.member_id if user.member_id else generate_member_id(db)
        ),  # Use provided member_id or generate one
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


def delete_user(db: Session, uuid: int):
    db_user = db.query(models.user.User).filter(models.user.User.uuid == uuid).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
