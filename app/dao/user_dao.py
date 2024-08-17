from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from app.database.crud import DataAccessLayer
from app.database.schemas.user import UserSchema
from app.dto.user_dto import AddUserDto
from app.enums.db_collections import DBCollections
from app.enums.http_config import HttpStatusCode
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId


class UserDAO:
    def __init__(self):
        self.__data_access_service = DataAccessLayer(
            model=UserSchema, collection_name=DBCollections.USER_MST.value)

    def get_all_users(self) -> list:
        return self.__data_access_service.get_all(
            search_by={"is_deleted": False})

    def add_user(self, user_model: AddUserDto) -> PyObjectId:
        try:
            return self.__data_access_service.add_one(user_model.dict())
        except DuplicateKeyError:
            raise HTTPException(status_code=HttpStatusCode.BAD_REQUEST,
                                detail="Username already exists")

    def delete_user_by_id(self, user_id: PyObjectId) -> int:
        return self.__data_access_service.update_one_set(
            search_by={"_id": AppUtils.bson_objectId_converter(user_id)},
            update_info={"is_deleted": True}
        )

    def get_user_dtl_by_id(self, user_id: PyObjectId) -> dict:
        return self.__data_access_service.get_by_id(
            primary_key=user_id)

    def get_user_dtl(self, filters: dict) -> dict:
        return self.__data_access_service.get_first_row_by_filter(filters)

    def update_user_dtl(self, user_id: PyObjectId,
                        update_info: dict) -> int:
        return self.__data_access_service.update_one_set(
            search_by={"_id": AppUtils.bson_objectId_converter(user_id)},
            update_info=update_info
        )
