from typing import Generator, List

from database.database import SessionLocal, get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from models.user import User
from sqlalchemy.orm import Session
from utils.auth import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Define the login endpoint


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """Retrieve the currently authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"message": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_access_token(token)
        if payload is None:
            raise credentials_exception
        user_uuid: int = payload.get("sub")
        if user_uuid is None:
            raise credentials_exception
        user = db.query(User).filter(User.uuid == user_uuid).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


class RequireRoles:
    def __getitem__(self, roles: List[str]):
        """Return a dependency that checks if the user has one of the required roles."""

        def dependency(current_user: User = Depends(get_current_user)) -> None:
            if current_user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "message": "You do not have the required permissions to access this resource."
                    },
                )

        return Depends(dependency)


# Instantiate the class for use
require_roles = RequireRoles()
