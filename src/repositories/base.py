from pydantic import BaseModel

from sqlalchemy import insert, select


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def add(self, data: BaseModel) -> BaseModel:
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        res = await self.session.execute(add_stmt)
        model = res.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def get_all(self) -> list[BaseModel]:
        query = select(self.model).order_by(self.model.id)
        res = await self.session.execute(query)
        models = res.scalars().all()
        return [self.schema.model_validate(model, from_attributes=True) for model in models]

    async def get_by_filter(self, **filter_by) -> list[BaseModel]:
        query = select(self.model).order_by(self.model.id).filter_by(**filter_by)
        res = await self.session.execute(query)
        models = res.scalars().all()
        return [self.schema.model_validate(model, from_attributes=True) for model in models]