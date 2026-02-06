from backend.modules import (
    TIMESTAMP,
    ForeignKey,
    Mapped,
    String,
    datetime,
    mapped_column,
)

from .base import Base


class Sessions(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"))
    refreshToken: Mapped[str] = mapped_column(String(500), nullable=True)
    createdAt: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=False), default=datetime.now()
    )
    updatedAt: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=False), onupdate=datetime.now(), default=datetime.now()
    )
