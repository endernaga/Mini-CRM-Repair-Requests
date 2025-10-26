from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.ticket_crud import TicketCRUD
from app.models import User
from app.models.db_settings import get_db
from app.models.ticket import TicketStatus
from app.schemas.ticket_schema import OpenTicketCreate, TicketRead
from app.utils.dependencies import get_current_user, get_current_user_admin

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/open", response_model=TicketRead)
async def open_ticket(
    ticket_data: OpenTicketCreate, db: AsyncSession = Depends(get_db)
):
    ticket = await TicketCRUD.create_ticket(db, ticket_data)
    return ticket


@router.get("/")
async def list_tickets(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    status: str | None = Query(None),
    title: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not user.is_admin:
        tickets, total = await TicketCRUD.get_tickets_filtered(
            db, page, per_page, status, user.id, title=title
        )
    else:
        tickets, total = await TicketCRUD.get_tickets_filtered(
            db, page, per_page, status, title=title
        )
    total_pages = (total + per_page - 1) // per_page

    return {
        "items": tickets,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_items": total,
            "total_pages": total_pages,
            "count": len(tickets),
        },
    }


@router.get(
    "/unassigned_tickets",
)
async def list_unassigned_tickets(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(
        10, ge=1, le=100, description="Tickets count per page"
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_admin),
):
    tickets, total = await TicketCRUD.list_unassigned_tickets(db, page, per_page)
    total_pages = (total + per_page - 1) // per_page

    return {
        "items": tickets,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_items": total,
            "total_pages": total_pages,
            "count": len(tickets),
        },
    }


@router.patch("/{ticket_id}/status")
async def update_ticket_status(
    ticket_id: UUID,
    new_status: TicketStatus = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    ticket = await TicketCRUD.update_ticket_status(db, ticket_id, new_status, user.id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"id": str(ticket.id), "status": ticket.status}


@router.patch("/{ticket_id}/assign")
async def assign_worker_to_ticket(
    ticket_id: UUID,
    worker_id: UUID = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_admin),
):
    ticket = await TicketCRUD.assign_worker(db, ticket_id, worker_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {
        "id": str(ticket.id),
        "worker_id": str(ticket.worker_id),
        "message": "Worker assigned successfully",
    }
