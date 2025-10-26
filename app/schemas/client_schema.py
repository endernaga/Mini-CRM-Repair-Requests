from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

PHONE_REGEX = r"^\+?\d{9,15}$"


class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    contact_location: str
    phone: str = Field(..., pattern=PHONE_REGEX)


class ClientRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    contact_location: str
    phone: str = Field(..., pattern=PHONE_REGEX)

    class Config:
        orm_mode = True
