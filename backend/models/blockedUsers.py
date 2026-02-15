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


class BlockedUsers(Base):
    __tablename__ = "blocked_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"))
    blockedBy: Mapped[int] = mapped_column(ForeignKey("users.id"))
    createdAt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetimeUTC()
    )

    def __repr__(self) -> str:
        return f"BlockedUser(postsID={self.userID!r}, blockedBy={self.blockedBy!r})"
