from backend.modules import (
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


class Likes(Base):
    __tablename__ = "likes"
    id: Mapped[int] = mapped_column(primary_key=True)
    postID: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"Follower(postsID={self.postID!r}, userID={self.userID!r})"
