import os

from app.database.database import DBClient
from app.database.schemas import PyObjectId
from app.utils.app_utils import AppUtils

DB_NAME = os.environ["DB_NAME"]


class DataAccessLayer:
    def __init__(self, model, collection_name: str):
        db_instance = DBClient.get_instance()
        self.__db_client = db_instance.client[DB_NAME][collection_name]
        self.__model = model

    def get_by_id(self, primary_key: PyObjectId,
                  project_by: dict = None) -> dict:
        print(f"primary_key: {primary_key}, project_by: {project_by}")
        search_by = {
            "_id": AppUtils.bson_objectId_converter(primary_key),
            "is_deleted": False
        }
        result: dict = self.__db_client.find_one(search_by, project_by)
        print(f"result: {result}")
        return result

    def get_all(self, search_by: dict, project_by: dict = None) -> list:
        print(f"search_by: {search_by}, project_by: {project_by}")
        result: list = list(self.__db_client.find(search_by, project_by))
        print(f"result: {result}")
        return result

    def add_one(self, obj_in: dict) -> PyObjectId:
        print(f"obj_in: {obj_in}")
        db_obj = self.__model(**obj_in).dict()
        result = self.__db_client.insert_one(db_obj)
        result_id = result.inserted_id
        print(f"result_id: {result_id}")
        return result_id

    def update_one_set(self, search_by: dict, update_info: dict) -> int:
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
        print(f"result: {result}")
        return result
