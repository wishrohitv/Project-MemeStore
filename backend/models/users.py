from backend.modules import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Optional,
    String,
    List,
    TIMESTAMP,
    relationship,
    ForeignKey,
    datetime,
    Enum,
)


from .base import Base
from .profile import Profile
from .enums import AccountStatus


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    userName: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(40))
    password: Mapped[bytes]
    joinDate: Mapped[str] = mapped_column(
        "timestamp", TIMESTAMP(timezone=False), nullable=False, default=datetime.now()
    )
    role: Mapped[int] = mapped_column(ForeignKey("role.id"), default=3)
    accountStatus: Mapped[AccountStatus] = mapped_column(
        Enum(AccountStatus), default=AccountStatus.active
    )
    profile: Mapped["Profile"] = relationship(backref="profile", uselist=False)

    def __repr__(self) -> str:
        return f"""Users(id={self.id!r},
                name={self.name!r},
                userName={self.userName!r}
                email={self.email!r},
                joinDate={self.joinDate!r},
                role={self.role!r},
                password{self.password!r},
                accountStatus={self.accountStatus!r},
            )"""
