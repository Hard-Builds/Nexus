from enum import Enum


class UserRolesEnum(Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class UserActiveStatusEnum(Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
