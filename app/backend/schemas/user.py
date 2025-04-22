from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = None
    role: Optional[Literal["admin", "user", "moderator"]] = "user"  # Add role field


class UserCreate(UserBase):
    password: str
    details: Optional[Dict[str, Any]] = {}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None
    details: Optional[Dict[str, Any]] = {}


class User(UserBase):
    uuid: str
    details: Dict[str, Any] = {}

    class Config:
        from_attributes = True
