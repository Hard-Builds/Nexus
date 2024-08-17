from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from app.database.crud import DataAccessLayer
from app.database.schemas.credential import CredentialSchema
from app.dto.credential import CreateCredentialDto
from app.enums.db_collections import DBCollections
from app.enums.http_config import HttpStatusCode
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId


class CredentialDAO:
    def __init__(self):
        self.__data_access_service = DataAccessLayer(
            model=CredentialSchema,
            collection_name=DBCollections.CREDENTIAL_MST.value
        )

    def add_credential(self, model: CreateCredentialDto) -> PyObjectId:
        try:
            return self.__data_access_service.add_one(model.dict())
        except DuplicateKeyError:
            raise HTTPException(status_code=HttpStatusCode.BAD_REQUEST,
                                detail="Username already exists")

    def get_credential_dtl(self, cred_id: PyObjectId) -> dict:
        cred_dtl: dict = self.__data_access_service.get_by_id(
            primary_key=cred_id)
        return cred_dtl

    def delete_by_id(self, credential_id: PyObjectId) -> int:
        search_by = {"_id": AppUtils.bson_objectId_converter(credential_id)}
        update_info = {"is_deleted": True}
        modified_count = self.__data_access_service.update_one_set(
            search_by=search_by,
            update_info=update_info
        )
        return modified_count
