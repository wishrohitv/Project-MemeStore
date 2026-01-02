"""
User created collection post
"""

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


class CollectionData(Base):
    __tablename__ = "collection_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    collectionID: Mapped[int] = mapped_column(ForeignKey("collections.id"))
    postID: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now())
    updatedAt: Mapped[datetime] = mapped_column(
        TIMESTAMP, onupdate=datetime.now(), default=datetime.now()
    )

    def __repr__(self):
        return f"""CollectionData(
                id={self.id!r},
                collectionId={self.collectionID!r},
                postId={self.postID!r},
                createdAt={self.createdAt!r},
                updatedAt={self.updatedAt!r}
            )"""
