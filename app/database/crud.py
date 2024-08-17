import os
from typing import Optional

from pymongo import IndexModel
from pymongo.errors import OperationFailure

from app.database.database import DBClient
from app.database.pipeline_builder import MongoPipelineBuilder
from app.enums.os_vars import OSVarsEnum
from app.middleware.context import RequestContext
from app.utils.DateUtils import DateUtils
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId

DB_NAME = os.environ[OSVarsEnum.DB_NAME.value]


class DataAccessLayer:
    def __init__(self, model, collection_name: str):
        db_instance = DBClient.get_instance()
        self.__db_client = db_instance.client[DB_NAME][collection_name]
        self.__model = model

    def handle_indexes(self, indexes: list[IndexModel]) -> None:
        existing_indexes: set = self.list_existing_indexes()

        """Generating New Indexes"""
        for index in indexes:
            index_name = index.document['name']
            try:
                if index_name not in existing_indexes:
                    self.__db_client.create_indexes([index])
                    print(f"Created index: {index_name}")
                else:
                    print(f"{index_name} Index Already exists!")
                    existing_indexes.remove(index_name)
            except OperationFailure as e:
                print(f"Failed to create index {index_name}: {e}")

        """Dropping Obsolete Indexes"""
        for index_name in existing_indexes:
            try:
                self.__db_client.drop_index(index_name)
                print(f"Dropped index: {index_name}")
            except OperationFailure as e:
                print(f"Failed to drop index {index_name}: {e}")

    def list_existing_indexes(self) -> set:
        indexes = self.__db_client.list_indexes()
        indexes: set = set(map(lambda x: x["name"], indexes))
        return indexes

    def get_by_id(self, primary_key: PyObjectId,
                  project_by: dict = None) -> dict:
        print(f"primary_key: {primary_key}, project_by: {project_by}")
        search_by = {
            "_id": AppUtils.bson_objectId_converter(primary_key),
            "is_deleted": False
        }
        result: dict = self.__db_client.find_one(search_by, project_by)
        result: dict = AppUtils.convert_object_id_to_str(result)
        print(f"result: {result}")
        return result

    def get_all(self, search_by: dict, project_by: dict = None) -> list:
        print(f"search_by: {search_by}, project_by: {project_by}")
        result: list = list(self.__db_client.find(search_by, project_by))
        result: list = AppUtils.convert_object_id_to_str(result)
        print(f"result: {result}")
        return result

    def add_one(self, obj_in: dict) -> PyObjectId:
        print(f"obj_in: {obj_in}")
        db_obj = self.__model(**obj_in).dict()
        print(f"db_obj: {db_obj}")
        result = self.__db_client.insert_one(db_obj)
        result_id = result.inserted_id
        print(f"result_id: {result_id}")
        return result_id

    def update_one_set(self, search_by: dict, update_info: dict) -> int:
        update_info.update({
            "modified_on": DateUtils.get_current_epoch(),
            "modified_by": RequestContext.get_context_user_id()
        })
        print(f"search_by: {search_by}, update_info: {update_info}")
        result = self.__db_client.update_one(
            filter=search_by,
            update={"$set": update_info}
        )
        modified_count = result.modified_count
        print(f"modified_count: {modified_count}")
        return modified_count

    def get_first_row_by_filter(self, search_by: dict,
                                project_by: dict = None) -> dict:
        result: dict = self.__db_client.find_one(search_by, project_by)
        result: dict = AppUtils.convert_object_id_to_str(result)
        print(f"result: {result}")
        return result

    def pipeline_aggregation(
            self, pipeline: list[MongoPipelineBuilder]) -> Optional[list]:
        print(f"pipeline: {pipeline}")
        result_list: list = list(self.__db_client.aggregate(pipeline))
        result_list: list = AppUtils.convert_object_id_to_str(result_list)
        print(f"result_list: {result_list}")
        return result_list