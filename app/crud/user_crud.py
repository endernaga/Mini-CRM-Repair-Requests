from uuid import UUID

from sqlalchemy import delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.utils.security import hash_password


class UserCRUD:
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hash_password(user_data.password),
            is_admin=user_data.is_admin,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def get_users(
            db: AsyncSession, page: int = 1, per_page: int = 10
    ) -> tuple[list[User], int]:
        offset = (page - 1) * per_page

        total = await db.scalar(select(func.count()).select_from(User))

        result = await db.execute(
            select(User)
            .offset(offset)
            .limit(per_page)
        )

        users = result.scalars().all()
        return users, total

    @staticmethod
    async def get_user(db: AsyncSession, user_id: UUID) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def update_user(
        db: AsyncSession, user_id: int, user_data: UserUpdate
    ) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalars().first()
        if not db_user:
            return None

        # Оновлюємо лише передані поля
        if user_data.name is not None:
            db_user.name = user_data.name
        if user_data.email is not None:
            db_user.email = user_data.email
        if user_data.password is not None:
            db_user.password = hash_password(user_data.password)
        if user_data.is_admin is not None:
            db_user.is_admin = user_data.is_admin

        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalars().first()
        if not db_user:
            return False

        await db.delete(db_user)
        await db.commit()
        return True
