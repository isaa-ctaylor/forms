import uuid

from database.database import Base
from sqlalchemy import JSON, Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        String(36), unique=True, index=True, default=lambda: str(uuid.uuid4())
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    details = Column(JSON, default={})
    timestamp = Column(String, nullable=False)

    user = relationship("User", back_populates="audits")
