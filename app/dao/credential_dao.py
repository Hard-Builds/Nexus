from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from app.database.crud import DataAccessLayer
from app.database.schemas import PyObjectId
from app.database.schemas.credential import CredentialSchema
from app.dto.credential import CreateCredentialDto
from app.enums.http_config import HttpStatusCode


class CredentialDAO:
    def __init__(self):
        self.__data_access_service = DataAccessLayer(
            model=CredentialSchema, collection_name="credential_mst")

    def add_credential(self, model: CreateCredentialDto) -> PyObjectId:
        try:
            return self.__data_access_service.add_one(model.dict())
        except DuplicateKeyError:
            raise HTTPException(status_code=HttpStatusCode.BAD_REQUEST,
                                detail="Username already exists")
