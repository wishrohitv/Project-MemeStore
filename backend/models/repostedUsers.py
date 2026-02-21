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
from backend.utils import datetimeUTC

from .base import Base


class ReportedUsers(Base):
    __tablename__ = "reported_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    reportedBy: Mapped[int] = mapped_column(ForeignKey("users.id"))
    userID: Mapped[int] = mapped_column(ForeignKey("users.id"))
    isResolved: Mapped[bool] = mapped_column(default=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetimeUTC()
    )
    updatedAt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetimeUTC(), onupdate=datetimeUTC()
    )

    def __repr__(self) -> str:
        return f"""ReportedUser(
                        id={self.id}
                        userID={self.userID!r},
                        reportedBy={self.reportedBy!r}),
                        isResolved={self.isResolved!r},
                        description={self.isResolved!r},
                        createdAt={self.createdAt!r}
                        updatedAt={self.updatedAt!r}
                    """
