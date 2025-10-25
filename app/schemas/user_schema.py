import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False


class UserRead(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    is_admin: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

class PaginatedUsers(BaseModel):
    items: list[UserRead]
    pagination: dict


