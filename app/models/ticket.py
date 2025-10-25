import uuid
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.db_settings import Base


class TicketStatus(PyEnum):
    NEW = "new"
    PROGRES = "progress"
    DONE = "done"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(TicketStatus), nullable=False, default=TicketStatus.NEW)

    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    worker_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    client = relationship("Client", back_populates="tickets")
    worker = relationship("User", back_populates="tickets")
