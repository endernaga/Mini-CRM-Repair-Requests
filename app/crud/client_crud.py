from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.client import Client
from app.utils.security import hash_password


class ClientCRUD:
    @staticmethod
    async def create_client(db: AsyncSession, client_data):
        result = await db.execute(
            select(Client).where(
                and_(
                    Client.name == client_data.name,
                    Client.email == client_data.email,
                    Client.contact_location == client_data.contact_location,
                    Client.phone == client_data.phone,
                )
            )
        )
        existing_client = result.scalars().first()

        if existing_client:
            return existing_client

        db_client = Client(
            name=client_data.name,
            email=client_data.email,
            contact_location=client_data.contact_location,
            phone=client_data.phone,
        )
        db.add(db_client)
        await db.commit()
        await db.refresh(db_client)
        return db_client

    @staticmethod
    async def get_client(db: AsyncSession, client_id):
        result = await db.execute(select(Client).where(Client.id == client_id))
        return result.scalars().first()

    @staticmethod
    async def list_clients(db: AsyncSession):
        result = await db.execute(select(Client))
        return result.scalars().all()
