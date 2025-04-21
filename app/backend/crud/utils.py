import bcrypt
from models.user import User
from sqlalchemy import func
from sqlalchemy.orm import Session


def generate_member_id(db: Session) -> str:
    max_member_id = db.query(func.max(User.member_id)).scalar()
    if max_member_id is None:
        return "0000"
    else:
        next_id = int(max_member_id) + 1
        return f"{next_id:04d}"


def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
