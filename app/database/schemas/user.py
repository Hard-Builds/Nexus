from typing import Optional

from pydantic import validator, EmailStr, SecretStr

from app.database.schemas import PyDanticBaseModel
from app.enums.user_enum import UserRolesEnum, UserActiveStatusEnum
from app.utils.password_utils import PasswordUtils


class UserSchema(PyDanticBaseModel):
    name: str
    username: EmailStr
    password: SecretStr
    role: Optional[UserRolesEnum] = UserRolesEnum.MEMBER.value
    active_status: Optional[
        UserActiveStatusEnum] = UserActiveStatusEnum.ACTIVE.value

    @validator("password")
    def hash_password(cls, value: str) -> str:
        """Hash the password before storing it in the model."""
        return PasswordUtils.get_password_hash(value.get_secret_value())

