from app.database.crud import DataAccessLayer
from app.database.schemas.app import AppSchema
from app.dto.app_dto import AddAppDto
from app.enums.db_collections import DBCollections
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId


class AppDao:
    def __init__(self):
        self.__data_access_service = DataAccessLayer(
            model=AppSchema, collection_name=DBCollections.APP_MST.value)

    def add_user(self, model: AddAppDto) -> PyObjectId:
        return self.__data_access_service.add_one(model.dict())

    def get_app_dtls(self, app_id: PyObjectId) -> dict:
        return self.__data_access_service.get_first_row_by_filter(
            search_by={
                "_id": AppUtils.bson_objectId_converter(app_id),
                "is_deleted": False
            })

    def update_app_by_id(self, app_id: PyObjectId, update_info: dict) -> int:
        return self.__data_access_service.update_one_set(
            search_by={"_id": AppUtils.bson_objectId_converter(app_id)},
            update_info=update_info
        )
