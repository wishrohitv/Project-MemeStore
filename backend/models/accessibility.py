from backend.modules import (
    ARRAY,
    BOOLEAN,
    INTEGER,
    JSON,
    JSONB,
    TIMESTAMP,
    ForeignKey,
    List,
    Mapped,
    Optional,
    String,
    mapped_column,
    relationship,
)

from .base import Base


class Accessibility(Base):
    __tablename__ = "accessibility"
    id: Mapped[int] = mapped_column(primary_key=True)
    endpointID: Mapped[str] = mapped_column(ForeignKey("endpoint.id"))
    roles: Mapped[JSONB] = mapped_column(JSONB, default=[])  # LIST ITEM
    partialAccess: Mapped[BOOLEAN] = mapped_column(BOOLEAN, default=False)

    def __repr__(self) -> str:
        return f"Accessibility(id={self.id!r}, endpoint_id={self.endpointID!r}, roles={self.roles!r})"
