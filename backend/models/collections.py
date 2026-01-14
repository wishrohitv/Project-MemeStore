"""
Alchemy model for collection, User create their own collection
"""

from sqlalchemy.orm.collections import MappedCollection
from sqlalchemy.sql.expression import null

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


class Collections(Base):
    __tablename__ = "collections"
    id: Mapped[int] = mapped_column(primary_key=True)
    collectionName: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    owner: Mapped[int] = mapped_column(ForeignKey("users.id"))
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now())
    updatedAt: Mapped[datetime] = mapped_column(
        TIMESTAMP, onupdate=datetime.now(), default=datetime.now()
    )

    def __repr__(self):
        return f"""Collections(
                id={self.id!r},
                collectionName={self.collectionName!r},
                description={self.description!r},
                owner={self.owner!r},
                createdAt={self.createdAt!r},
                updatedAt={self.updatedAt!r}
            )"""
