
from app.database.crud import DataAccessLayer
from app.database.schemas import PyObjectId
from app.database.schemas.user import UserSchema
from app.dto.user import AddUserDto
from app.utils.DateUtils import DateUtils
from app.utils.app_utils import AppUtils


class UserDAO:
    def __init__(self):
        self.__data_access_service = DataAccessLayer(
            model=UserSchema, collection_name="user_mst")

    def get_all_users(self) -> list:
        return self.__data_access_service.get_all(
            search_by={"is_deleted": False})

    def add_user(self, user_model: AddUserDto) -> PyObjectId:
        return self.__data_access_service.add_one(user_model.dict())

    def delete_user_by_id(self, user_id: PyObjectId) -> int:
        return self.__data_access_service.update_one_set(
            search_by={"_id": AppUtils.bson_objectId_converter(user_id)},
            update_info={
                "is_deleted": True,
                "modified_on": DateUtils.get_current_epoch()
            }
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
