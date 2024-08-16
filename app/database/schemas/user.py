from app.database.schemas import PyDanticBaseModel
from app.enums.user import UserRolesEnum, UserActiveStatusEnum


class UserSchema(PyDanticBaseModel):
    username: str
    password: str
    role: UserRolesEnum = UserRolesEnum.MEMBER
    ActiveStatus: UserActiveStatusEnum = UserActiveStatusEnum.ACTIVE
