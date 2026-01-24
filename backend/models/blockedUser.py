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

from .base import Base


class BlockedUser(Base):
    __tablename__ = "blocked_user"
    id: Mapped[int] = mapped_column(primary_key=True)
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"))
    blockedBy: Mapped[int] = mapped_column(ForeignKey("users.id"))
    createdAt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), default=datetime.now()
    )

    def __repr__(self) -> str:
        return f"BlockedUser(postsID={self.userID!r}, blockedBy={self.blockedBy!r})"
