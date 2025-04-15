from fastapi import APIRouter

from src.database import async_session_maker
from src.repositories.clients import ClientsRepository
from src.schemas.clients import ClientAdd

router = APIRouter(prefix="/clients", tags=["Клиенты"])


@router.get("/all")
async def get_clients():
    async with async_session_maker() as session:
        clients = await ClientsRepository(session).get_all()
    return clients

@router.get("/filter_by")
async def get_clients(nums: str):
    async with async_session_maker() as session:
        clients = await ClientsRepository(session).get_by_filter(nums)
    return clients

@router.post("")
async def add_client(client: ClientAdd):
    async with async_session_maker() as session:
        client = await ClientsRepository(session).add(client)
        await session.commit()
    return client
