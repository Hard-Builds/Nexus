from app.database.crud import DataAccessLayer
from app.database.schemas.app import AppSchema
from app.dto.app_dto import AddAppDto
from app.enums.db_collections import DBCollections
from app.utils.pyobjectid import PyObjectId


class AppDao:
    def __init__(self):
        self.__data_access_service = DataAccessLayer(
            model=AppSchema, collection_name=DBCollections.APP_MST.value)

    def add_user(self, model: AddAppDto) -> PyObjectId:
        return self.__data_access_service.add_one(model.dict())
