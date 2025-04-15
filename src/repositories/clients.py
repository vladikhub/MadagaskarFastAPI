from sqlalchemy import select

from src.models.clients import ClientsModel
from src.repositories.base import BaseRepository
from src.schemas.clients import Client


class ClientsRepository(BaseRepository):
    model = ClientsModel
    schema = Client

    async def get_by_filter(self, nums):
        query = select(self.model).filter(ClientsModel.phone.ilike(f"%{nums}"))
        res = await self.session.execute(query)
        models = res.scalars().all()
        return [self.schema.model_validate(model, from_attributes=True) for model in models]