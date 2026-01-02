from backend.modules import (
    TIMESTAMP,
    Enum,
    ForeignKey,
    List,
    Mapped,
    Optional,
    String,
    mapped_column,
    relationship,
)

from .base import Base
from .enums import AgeRating


class Posts(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    tags: Mapped[str] = mapped_column(String(100), nullable=True)
    mediaUrl: Mapped[str] = mapped_column(nullable=True)
    mediaPublicID: Mapped[str] = mapped_column(String(55), nullable=True)
    fileType: Mapped[str] = mapped_column(String(8), nullable=False)
    fileExtension: Mapped[str] = mapped_column(String(5))
    visibility: Mapped[bool] = mapped_column(default=True)
    ageRating: Mapped[AgeRating] = mapped_column(
        "ageRating",
        Enum(AgeRating),
        default=AgeRating.pg13,  # 'pg13' age ratings on posts by default
        quote=True,
    )
    category: Mapped[int] = mapped_column(ForeignKey("category.id"))

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
                )"""
