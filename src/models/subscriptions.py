import datetime
import enum
from sqlalchemy import DateTime, func, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from src.database import Base
from src.enums.subscriptions import SubscriptionType, PeriodType

if TYPE_CHECKING:
    from src.models.clients import ClientsModel


class SubscriptionsModel(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(unique=True)
    type: Mapped[str] = mapped_column(Enum(SubscriptionType))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    client: Mapped["ClientsModel"] = relationship(back_populates="subscription")


class MinuteSubscriptionsModel(SubscriptionsModel):
    __tablename__ = "minute_subscriptions"

    id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id", ondelete="CASCADE"), primary_key=True)
    minutes: Mapped[int] = mapped_column(nullable=True)


class UnlimitedSubscriptionsModel(SubscriptionsModel):
    __tablename__ = "unlimited_subscriptions"

    id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"), primary_key=True)
    period: Mapped[str]
    end_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

