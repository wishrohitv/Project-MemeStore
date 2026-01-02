from backend.modules import (
    Mapped,
    mapped_column,
    Optional,
    String,
    List,
    TIMESTAMP,
    relationship,
    ForeignKey,
    datetime,
)
from .base import Base


class Templates(Base):
    __tablename__ = "templates"
    id: Mapped[int] = mapped_column(primary_key=True)
    postID: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"))
    createAt: Mapped[str] = mapped_column(
        "timestamp", TIMESTAMP(timezone=False), nullable=False, default=datetime.now()
    )
