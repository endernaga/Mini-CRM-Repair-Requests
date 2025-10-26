from http.client import HTTPException
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud.user_crud import UserCRUD
from app.models import User
from app.models.db_settings import get_db
from app.schemas.user_schema import (PaginatedUsers, UserCreate, UserRead,
                                     UserUpdate)
from app.utils.dependencies import get_current_user_admin

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    user_auth: User = Depends(get_current_user_admin),
):
    db_user = await UserCRUD.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    return await UserCRUD.create_user(db, user)


@router.get("/", response_model=PaginatedUsers)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(
        10, ge=1, le=100, description="Users count per page"
    ),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_admin),
):
    users, total = await UserCRUD.get_users(db, page=page, per_page=per_page)
    total_pages = (total + per_page - 1) // per_page

    return {
        "items": users,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_items": total,
            "total_pages": total_pages,
            "count": len(users),
        },
    }


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_admin),
):
    db_user = await UserCRUD.get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db),
    user_auth: User = Depends(get_current_user_admin),
):
    db_user = await UserCRUD.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_admin),
):
    success = await UserCRUD.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
