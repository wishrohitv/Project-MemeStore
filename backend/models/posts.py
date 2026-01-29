from sqlalchemy.sql.expression import nullsfirst

from backend.modules import (
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

from .base import Base
from .enums import AgeRating


class Posts(Base):
    """
    This post table stores post and its replies and reposted posts
    - when parentPostID is None(null) and isReposted will be always false (because its original post) then it will be considered original post
    - if parentPostID is post id and isReposted is true then it will be considered reposted post
    -  if parentPostID is post id and isReposted is false then is will be considered replies
    """

    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    tags: Mapped[str] = mapped_column(String(100), nullable=True)
    mediaUrl: Mapped[str] = mapped_column(nullable=True)
    mediaPublicID: Mapped[str] = mapped_column(String(55), nullable=True)
    fileType: Mapped[str] = mapped_column(String(8), nullable=True)
    fileExtension: Mapped[str] = mapped_column(String(5), nullable=True)
    visibility: Mapped[bool] = mapped_column(default=True)
    parentPostID: Mapped[int] = mapped_column(default=None, nullable=True)
    isReposted: Mapped[bool] = mapped_column(default=False, nullable=False)
    ageRating: Mapped[AgeRating] = mapped_column(
        "ageRating",
        Enum(AgeRating),
        default=AgeRating.pg13,  # 'pg13' age ratings on posts by default
        quote=True,
    )
    category: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        default=datetime.now(),
    )
    updatedAt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        onupdate=datetime.now(),
        default=datetime.now(),
    )

    def __repr__(self) -> str:
        return f"""Posts(
                    'id': {self.id!r},
                    'userID': {self.userID!r},
                    'title': {self.title!r},
                    'tags': {self.tags!r},
                    'mediaUrl': {self.mediaUrl!r},
                    'mediaPublicID': {self.mediaPublicID!r},
                    'fileType': {self.fileType!r},
                    'fileExtension': {self.fileExtension!r},
                    'visibility': {self.visibility!r},
                    'ageRating': {self.ageRating!r},
                    'category': {self.category!r},
                    'createdAt': {self.createdAt!r},
                    'updatedAt': {self.updatedAt!r},
                )"""
