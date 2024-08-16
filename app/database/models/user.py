from sqlalchemy import Column, String, Enum

from app.database.models import SQLAbstractBaseModel
from app.enums.user import UserActiveStatusEnum, UserRolesEnum
from app.utils.password_utils import PasswordUtils


class User(SQLAbstractBaseModel):
    __tablename__ = "user"

    username = Column(String(255), unique=True, index=True, nullable=False)
    _hashed_password = Column("password", String(255), nullable=False)

    role = Column(Enum(UserRolesEnum), default=UserRolesEnum.MEMBER)
    ActiveStatus = Column(Enum(UserActiveStatusEnum),
                          default=UserActiveStatusEnum.ACTIVE)

    @property
    def user_password(self):
        raise AttributeError("Password is not readable.")

    @user_password.setter
    def password(self, plain_password: str):
        self._hashed_password = PasswordUtils.get_password_hash(plain_password)
