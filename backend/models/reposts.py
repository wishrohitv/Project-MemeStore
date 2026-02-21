from backend.modules import (
    TIMESTAMP,
    ForeignKey,
    Integer,
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


class Reposts(Base):
    """
    Represents a repost of a post by a user.
    """

    __tablename__ = "reposts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    userID: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    postID: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetimeUTC
    )

    def __repr__(self):
        return f"Repost(id={self.id}, user_id={self.userID}, post_id={self.postID}, created_at={self.createdAt})"
