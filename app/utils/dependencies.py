from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_settings import get_db
from app.models.user import User

from .jwt import decode_token

api_key_header = APIKeyHeader(name="Authorization")


async def get_current_user(
    token: str = Depends(api_key_header), db: AsyncSession = Depends(get_db)
) -> User:
    if not token.startswith("Bearer"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    if token.startswith("Bearer "):
        token = token[7:]
    payload = decode_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    result = await db.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


async def get_current_user_admin(
    token: str = Depends(api_key_header), db: AsyncSession = Depends(get_db)
) -> User:
    user = await get_current_user(token, db)

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    return user
