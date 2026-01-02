from backend.modules import datetime

from  backend.modules import (
    Mapped,
    mapped_column,
    Optional,
    String,
    List,
    TIMESTAMP,
    relationship,
    ForeignKey,
)

from .base import Base

class Follower(Base):
    __tablename__ = "follower"
    id : Mapped[int] = mapped_column(primary_key=True)
    userID : Mapped[int] = mapped_column(ForeignKey("users.id"))
    followerID : Mapped[int] = mapped_column(ForeignKey("users.id"))
    timestamp : Mapped[str] = mapped_column('timestamp', TIMESTAMP(timezone=False), nullable=False, default=datetime.now())

    def __repr__(self) -> str:
        return f"""Follower(userID={self.userID!r}, 
        followerID={self.followerID!r},
        timeStamp={self.timestamp!r}
        )"""