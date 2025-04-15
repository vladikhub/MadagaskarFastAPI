import datetime

from sqlalchemy import select, insert

from src.models.clients import ClientsModel
from src.repositories.base import BaseRepository
from src.models.subscriptions import SubscriptionsModel, MinuteSubscriptionsModel, UnlimitedSubscriptionsModel
from src.schemas.subscriptions import Subscription, MinuteSubscriptionAdd, UnlimitedSubscriptionAdd


class SubscriptionsRepository(BaseRepository):
    model = SubscriptionsModel
    schema = Subscription


    async def get_by_client_id(self, client_id: int):
        query = (select(SubscriptionsModel)
                 .join(ClientsModel, ClientsModel.subscription_id == SubscriptionsModel.id)
                 .filter(ClientsModel.id == client_id))

        subscription = (await self.session.execute(query)).scalars().one_or_none()
        if not subscription:
            return None
        if subscription.type == "Минутный":
            query_full = select(MinuteSubscriptionsModel).filter(MinuteSubscriptionsModel.id == subscription.id)
        elif subscription.type == "Безлимитный":
            query_full = select(UnlimitedSubscriptionsModel).filter(UnlimitedSubscriptionsModel.id == subscription.id)
        full_sub = (await self.session.execute(query_full)).scalars().one()
        return full_sub

    async def add_minute_subscription(self, client_id: int, subscription_data: MinuteSubscriptionAdd):
        add_sub_stmt = insert(SubscriptionsModel).values(number=subscription_data.number, type=subscription_data.type).returning(SubscriptionsModel.id)
        sub_id = (await self.session.execute(add_sub_stmt)).scalar()
        add_min_sub_stmt = insert(MinuteSubscriptionsModel).values(id=sub_id, minutes=subscription_data.minutes)
        await self.session.execute(add_min_sub_stmt)
        query_client = select(ClientsModel).filter_by(id=client_id)
        client = (await self.session.execute(query_client)).scalars().one()
        if client:
            client.subscription_id = sub_id

    async def add_unlimited_subscription(self, client_id: int, subscription_data: UnlimitedSubscriptionAdd, end_at: datetime.datetime):
        add_sub_stmt = insert(SubscriptionsModel).values(number=subscription_data.number, type=subscription_data.type).returning(SubscriptionsModel.id)
        print(add_sub_stmt.compile(), "----------------------------------------------------------------------------------------------------")
        sub_id = (await self.session.execute(add_sub_stmt)).scalar()
        add_unlim_sub_stmt = insert(UnlimitedSubscriptionsModel).values(id=sub_id, period=subscription_data.period, end_at=end_at)
        print(add_unlim_sub_stmt.compile())
        await self.session.execute(add_unlim_sub_stmt)
        query_client = select(ClientsModel).filter_by(id=client_id)
        client = (await self.session.execute(query_client)).scalars().one()
        if client:
            client.subscription_id = sub_id