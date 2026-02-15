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
from backend.utils import datetimeUTC

from .base import Base
from .enums import AccountStatus
from .profile import Profile


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    userName: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(40))
    password: Mapped[bytes]
    createdAt: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=datetimeUTC()
    )
    role: Mapped[int] = mapped_column(ForeignKey("role.id"), default=3)
    accountStatus: Mapped[AccountStatus] = mapped_column(
        Enum(AccountStatus), default=AccountStatus.active
    )
    isVerified: Mapped[bool] = mapped_column(default=False)
    profile: Mapped["Profile"] = relationship(backref="profile", uselist=False)

    def __repr__(self) -> str:
        return f"""Users(id={self.id!r},
                name={self.name!r},
                userName={self.userName!r}
                email={self.email!r},
                createdAt={self.createdAt!r},
                role={self.role!r},
                password{self.password!r},
                accountStatus={self.accountStatus!r},
                isVerified={self.isVerified!r}
            )"""
