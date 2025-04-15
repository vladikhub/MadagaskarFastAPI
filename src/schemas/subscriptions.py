import datetime
from pydantic import BaseModel, Field

from src.enums.subscriptions import SubscriptionType, PeriodType


class SubscriptionAdd(BaseModel):
    number: int
    created_at: datetime.datetime
    type: SubscriptionType


class MinuteSubscriptionAdd(SubscriptionAdd):
    minutes: int
    type: SubscriptionType = SubscriptionType.MINUTE


class UnlimitedSubscriptionAdd(SubscriptionAdd):
    period: str
    end_at: datetime.datetime = Field(default=None)
    type: SubscriptionType = SubscriptionType.UNLIMITED


class Subscription(SubscriptionAdd):
    id: int
