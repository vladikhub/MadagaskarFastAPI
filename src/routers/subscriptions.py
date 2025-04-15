import datetime

from fastapi import APIRouter
from sqlalchemy import select
from dateutil.relativedelta import relativedelta

from src.database import async_session_maker
from src.repositories.subscriptions import SubscriptionsRepository
from src.models.subscriptions import SubscriptionsModel, MinuteSubscriptionsModel, UnlimitedSubscriptionsModel
from src.models.clients import ClientsModel
from src.schemas.subscriptions import MinuteSubscriptionAdd, UnlimitedSubscriptionAdd

router = APIRouter(prefix="/subscriptions", tags=["Абонементы"])

@router.get("", summary="Получить все абонементы")
async def get_subscriptions():
    async with async_session_maker() as session:
        subscriptions = await SubscriptionsRepository(session).get_all()
        return subscriptions

@router.get("/client_id", summary="Получить абонемент по id клиента")
async def get_by_client_id(client_id: int):
    async with async_session_maker() as session:
        subscription = await SubscriptionsRepository(session).get_by_client_id(client_id)
        return subscription

@router.post("/add-minute", summary="Добавить минутный абонемент клиенту")
async def add_minute_subscription_to_client(
        client_id: int,
        subscription_data: MinuteSubscriptionAdd
):
    async with async_session_maker() as session:
        await SubscriptionsRepository(session).add_minute_subscription(client_id, subscription_data)
        await session.commit()
    return {"success": "OK"}

@router.post("/add-unlimited", summary="Добавить безлимитный абонемент клиенту")
async def add_unlimited_subscription_to_client(
        client_id: int,
        subscription_data: UnlimitedSubscriptionAdd
):
    end_at =  datetime.datetime.now()
    if subscription_data.period == "Месяц":
        end_at += relativedelta(months=1)
    elif subscription_data.period == "Полгода":
        end_at += relativedelta(months=6)
    elif subscription_data.period == "Год":
        end_at += relativedelta(months=12)

    async with async_session_maker() as session:
        await SubscriptionsRepository(session).add_unlimited_subscription(client_id, subscription_data, end_at)
        await session.commit()
    return {"success": "OK"}

