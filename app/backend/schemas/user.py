from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = None


class UserCreate(UserBase):
    password: str
    member_id: Optional[str] = None


class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    uuid: str
    member_id: str

    class Config:
        from_attributes = True
