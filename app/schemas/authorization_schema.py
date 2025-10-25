from uuid import UUID

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: UUID | None = None


class Login(BaseModel):
    email: EmailStr
    password: str
