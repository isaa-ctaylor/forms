from typing import Any, Dict, Literal, Optional

from more_itertools import first
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = None
    role: Optional[Literal["admin", "user", "moderator"]] = "user"  # Add role field
    first_name: Optional[str] = None
    middle_names: Optional[str] = None
    last_name: Optional[str] = None


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
