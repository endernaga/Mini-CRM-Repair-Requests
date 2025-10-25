import uuid

from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.crud.client_crud import ClientCRUD
from app.models.client import Client
from app.models.ticket import Ticket, TicketStatus
from app.routers.user_route import get_user


class TicketCRUD:
    @staticmethod
    async def create_ticket(db: AsyncSession, ticket_data):
        if getattr(ticket_data, "client", None):
            client = await ClientCRUD.create_client(db, ticket_data.client)
        else:
            raise ValueError("Either client_id or client must be provided")

        ticket = Ticket(
            title=ticket_data.title,
            description=ticket_data.description,
            status=ticket_data.status or TicketStatus.NEW,
            client_id=client.id,
            worker_id=getattr(ticket_data, "worker_id", None),
        )

        db.add(ticket)
        await db.commit()
        await db.refresh(ticket, attribute_names=["client", "worker"])
        return ticket

    @staticmethod
    async def get_ticket(db: AsyncSession, ticket_id: uuid.UUID):
        result = await db.execute(
            select(Ticket)
            .options(selectinload(Ticket.client))
            .options(selectinload(Ticket.worker))
            .where(Ticket.id == ticket_id)
        )
        return result.scalars().first()

    @staticmethod
    async def get_tickets_filtered(
        db: AsyncSession,
        page: int = 1,
        per_page: int = 10,
        status: str | None = None,
        worker_id: str | None = None,
        title: str | None = None,
    ):
        query = select(Ticket)
        filters = []

        if status:
            filters.append(Ticket.status == status)
        if worker_id:
            filters.append(Ticket.worker_id == worker_id)
        if title:
            filters.append(Ticket.title.ilike(f"%{title}%"))

        if filters:
            query = query.where(and_(*filters))

        # total count
        total = await db.scalar(select(func.count()).select_from(query.subquery()))

        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        result = await db.execute(query)
        tickets = result.scalars().all()

        return tickets, total

    @staticmethod
    async def list_tickets(db: AsyncSession):
        result = await db.execute(
            select(Ticket)
            .options(selectinload(Ticket.client))
            .options(selectinload(Ticket.worker))
        )
        return result.scalars().all()

    @staticmethod
    async def list_workers_ticket(db: AsyncSession, worker_id):
        result = await db.execute(
            select(Ticket)
            .options(selectinload(Ticket.client))
            .options(selectinload(Ticket.worker))
            .where(Ticket.worker_id == worker_id)
        )

        return result.scalars().all()

    @staticmethod
    async def list_unassigned_tickets(db: AsyncSession, page: int = 1, per_page: int = 10):
        offset = (page - 1) * per_page

        total = await db.scalar(
            select(func.count()).select_from(Ticket).where(Ticket.worker_id == None)
        )

        result = await db.execute(
            select(Ticket)
            .options(selectinload(Ticket.client))
            .options(selectinload(Ticket.worker))
            .where(Ticket.worker_id == None)
            .offset(offset)
            .limit(per_page)
        )

        tickets = result.scalars().all()
        return tickets, total

    @staticmethod
    async def update_ticket_status(
        db: AsyncSession,
        ticket_id: uuid.UUID,
        new_status: TicketStatus,
        worker_id: uuid.UUID,
    ):
        worker = await get_user(worker_id)

        result = select(Ticket).where(Ticket.id == ticket_id)
        if not worker.is_admin:
            result = result.where(Ticket.worker_id == worker_id)

        ticket = result.scalars().first()
        if not ticket:
            return None

        ticket.status = new_status
        await db.commit()
        await db.refresh(ticket)
        return ticket

    @staticmethod
    async def assign_worker(
        db: AsyncSession, ticket_id: uuid.UUID, worker_id: uuid.UUID
    ):
        result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
        ticket = result.scalars().first()
        if not ticket:
            return None

        ticket.worker_id = worker_id
        await db.commit()
        await db.refresh(ticket)
        return ticket

    @staticmethod
    async def delete_ticket(db: AsyncSession, ticket_id: uuid.UUID):
        result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
        ticket = result.scalars().first()
        if not ticket:
            return False

        await db.delete(ticket)
        await db.commit()
        return True
