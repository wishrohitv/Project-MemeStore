from  backend.modules import (
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

class Category(Base):
    __tablename__ = "category"
    id : Mapped[int] = mapped_column(primary_key=True)
    category : Mapped[str] = mapped_column(String(50))

    def __repr__(self) -> str:
        return f"""Category(id={self.id!r}, category={self.category})"""