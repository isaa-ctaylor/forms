import uuid

from database.database import Base
from sqlalchemy import JSON, Boolean, Column, Integer, String, Enum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        String(36), unique=True, index=True, default=lambda: str(uuid.uuid4())
    )
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    details = Column(JSON, default={})
    role = Column(
        Enum("admin", "user", "moderator", name="user_roles"), default="user"
    )  # Add role field

    def __repr__(self):
        return (
            f"<User id={self.id}, uuid={self.uuid}, email='{self.email}', "
            f"details={self.details}, role={self.role}>"
        )
