from backend.modules import PyEnum


# Post's age ratings
class AgeRating(PyEnum.Enum):
    pg13 = "pg13"
    nsfw = "NSFW"


# Account's status
class AccountStatus(PyEnum.Enum):
    active = "active"
    suspended = "suspended"
    banned = "banned"
    deleted = "deleted"
