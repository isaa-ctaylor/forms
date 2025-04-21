import uuid

from database.database import Base
from sqlalchemy import Boolean, Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        String(36), unique=True, index=True, default=lambda: str(uuid.uuid4())
    )
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    member_id = Column(String(4), unique=True, index=True)

    def __repr__(self):
        return f"<User id={self.id}, uuid={self.uuid}, email='{self.email}', member_id='{self.member_id}'>"
