from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from src.database import Base
if TYPE_CHECKING:
    from src.models.subscriptions import SubscriptionsModel


class ClientsModel(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(18))
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id", ondelete="SET NULL"), nullable=True)

    subscription: Mapped["SubscriptionsModel"] = relationship(back_populates="client")