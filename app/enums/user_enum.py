from enum import StrEnum


class UserRolesEnum(StrEnum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class UserActiveStatusEnum(StrEnum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
