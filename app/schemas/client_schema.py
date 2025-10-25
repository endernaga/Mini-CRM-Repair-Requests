from uuid import UUID

from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    contact_location: str
    phone: str


class ClientRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    contact_location: str
    phone: str

    class Config:
        orm_mode = True
