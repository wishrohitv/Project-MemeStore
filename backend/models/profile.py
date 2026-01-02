from datetime import datetime

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.types import Integer

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


class Profile(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    bio: Mapped[str] = mapped_column(String(400), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    profileImage: Mapped[Optional[bytes]]
    country: Mapped[str] = mapped_column(String(40))

    def __repr__(self) -> str:
        return f"""Profile(id={self.id!r},
                profileImage={self.profileImage!r},
                country={self.country!r}
            )"""
