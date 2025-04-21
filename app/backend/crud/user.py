from models import user as user_model
from schemas import user as user_schema
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = user.password  # In a real application, hash the password!
    db_user = user_model.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: user_schema.UserCreate):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        db_user.email = user_update.email
        db_user.hashed_password = user_update.password  # Remember to hash in real apps!
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
