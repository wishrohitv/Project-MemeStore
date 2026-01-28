from backend.modules import (
    INTEGER,
    TIMESTAMP,
    ForeignKey,
    Mapped,
    String,
    datetime,
    mapped_column,
)

from .base import Base


class Comments(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    postID: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[int] = mapped_column(String(1000), nullable=False)
    parentCommentID: Mapped[int] = mapped_column(INTEGER, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), default=datetime.now()
    )
    updatedAt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), onupdate=datetime.now(), default=datetime.now()
    )

    def __repr__(self) -> str:
        return f"""
            Comments(
                id={self.id},
                postID={self.postID},
                userID={self.userID},
                content={self.content},
                parentCommentID={self.parentCommentID},
                createdAt={self.createdAt},
                updatedAt={self.updatedAt}
            )
            """
