from fastapi import HTTPException

from app.database.crud import DataAccessLayer
from app.database.models.user import User
from app.database.schemas.user import UserSchema
from app.dto.user import AddUserDto
from app.enums.http_config import HttpStatusCode
from app.utils.DateUtils import DateUtils


class UserDAO:
    def __init__(self):
        self.__data_access_service = DataAccessLayer(model=User)

    def get_all_users(self) -> list:
        return self.__data_access_service.get_all()

    def add_user(self, model: AddUserDto):
        return self.__data_access_service.add_row(model)

    def delete_user_by_id(self, user: User):
        user.is_deleted = True
        user.modified_on = DateUtils.get_current_timestamp()
        self.__data_access_service.update_row(user)

    def get_user_dtl_by_id(self, user_id: int):
        return self.__data_access_service.get_by_id(user_id)

    def get_user_dtl(self, filters):
        return self.__data_access_service.get_first_row_by_filter(filters)

    def update_user_dtl(self, user: User):
        user.modified_on = DateUtils.get_current_timestamp()
        return self.__data_access_service.update_row(user)
