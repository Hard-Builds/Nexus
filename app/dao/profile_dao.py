from app.database.crud import DataAccessLayer
from app.database.schemas.profile import ProfileSchema
from app.dto.profile_dto import CreateProfileDto
from app.enums.db_collections import DBCollections
from app.utils.pyobjectid import PyObjectId


class ProfileDAO:
    def __init__(self):
        self.__data_access_service = DataAccessLayer(
            model=ProfileSchema,
            collection_name=DBCollections.PROFILE_MST.value
        )

    def add_profile(self, model: CreateProfileDto) -> PyObjectId:
        return self.__data_access_service.add_one(model.dict())
