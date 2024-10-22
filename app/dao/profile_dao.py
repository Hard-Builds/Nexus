from typing import Optional

from app.database.crud import DataAccessLayer
from app.database.pipeline_builder import MongoPipelineBuilder
from app.database.schemas.profile import ProfileSchema
from app.dto.profile_dto import CreateProfileReqDto
from app.enums.db_collections import DBCollections
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId


class ProfileDAO:
    def __init__(self):
        self.__data_access_service = DataAccessLayer(
            model=ProfileSchema,
            collection_name=DBCollections.PROFILE_MST.value
        )

    def add_profile(self, model: CreateProfileReqDto) -> PyObjectId:
        return self.__data_access_service.add_one(model.dict())

    def get_profile(self, profile_id: PyObjectId) -> dict:
        return self.__data_access_service.get_first_row_by_filter(
            search_by={
                "_id": AppUtils.bson_objectId_converter(profile_id),
                "is_deleted": False
            }
        )

    def delete_profile(self, profile_id: PyObjectId) -> int:
        return self.__data_access_service.update_one_set(
            search_by={"_id": AppUtils.bson_objectId_converter(profile_id)},
            update_info={"is_deleted": True}
        )

    def update_profile(self, profile_id: PyObjectId,
                       update_info: dict) -> int:
        modified_count = self.__data_access_service.update_one_set(
            search_by={"_id": AppUtils.bson_objectId_converter(profile_id)},
            update_info=update_info
        )
        return modified_count

    def profile_pipeline_aggregation(
            self, pipeline: list[MongoPipelineBuilder]) -> Optional[list]:
        return self.__data_access_service.pipeline_aggregation(
            pipeline=pipeline)
