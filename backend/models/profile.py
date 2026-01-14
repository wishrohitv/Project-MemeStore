from backend.modules import (
    TIMESTAMP,
    ForeignKey,
    Integer,
    List,
    Mapped,
    Optional,
    String,
    mapped_column,
    relationship,
)

from .base import Base


class Profile(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    bio: Mapped[str] = mapped_column(String(400), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    mediaUrl: Mapped[str] = mapped_column(nullable=True)
    mediaPublicID: Mapped[str] = mapped_column(String(55), nullable=True)
    fileType: Mapped[str] = mapped_column(String(8), nullable=True)
    fileExtension: Mapped[str] = mapped_column(String(5), nullable=True)
    country: Mapped[str] = mapped_column(String(40))

    def __repr__(self) -> str:
        return f"""Profile(id={self.id!r},
                mediaUrl={self.mediaUrl!r},
                mediaPublicID={self.mediaPublicID!r},
                fileType={self.fileType!r},
                fileExtension={self.fileExtension!r},
                country={self.country!r}
            )"""
