from backend.modules import (
    TIMESTAMP,
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


class Follower(Base):
    __tablename__ = "follower"
    id: Mapped[int] = mapped_column(primary_key=True)
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"))
    followerID: Mapped[int] = mapped_column(ForeignKey("users.id"))
    createdAt: Mapped[str] = mapped_column(
        "timestamp", TIMESTAMP(timezone=True), default=datetimeUTC()
    )

    def __repr__(self) -> str:
        return f"""Follower(userID={self.userID!r},
        followerID={self.followerID!r},
        createdAt={self.createdAt!r}
        )"""
