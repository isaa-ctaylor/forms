import bcrypt
from fastapi import HTTPException, status
from models.user import User
from sqlalchemy import func
from sqlalchemy.orm import Session


def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def check_role(user: User, required_roles: list[str]):
    if user.role not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"You do not have the required permissions to access this resource."
            },
        )
    return True
