import uuid

from pydantic import BaseModel

from app.models.ticket import TicketStatus
from app.schemas.client_schema import ClientCreate, ClientRead
from app.schemas.user_schema import UserRead


class OpenTicketCreate(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    status: TicketStatus
    client: ClientCreate


class TicketRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    status: str
    client: ClientRead
    worker: UserRead | None = None

    class Config:
        from_attributes = True
