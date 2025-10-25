from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.utils.security import verify_password


class AuthCRUD:
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()

        if not user:
            return None

        if not verify_password(password, user.password):
            return None
        return user
