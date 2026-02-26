from backend.modules import (
    JSON,
    TIMESTAMP,
    Enum,
    ForeignKey,
    List,
    Mapped,
    Optional,
    String,
    datetime,
    mapped_column,
    relationship,
)
from backend.utils import datetimeUTC

from .base import Base
from .enums import NotificationType


class Notifications(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(TIMESTAMP, primary_key=True, default=datetimeUTC)
    userId: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType), nullable=False
    )
    notice: Mapped[JSON] = mapped_column(JSON, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetimeUTC)
    updatedAt: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetimeUTC, onupdate=datetimeUTC
    )
    readAt: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    deletedAt: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
