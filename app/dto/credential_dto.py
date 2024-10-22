from typing import Optional

from pydantic import BaseModel, SecretStr

from app.enums.user_enum import UserRolesEnum
from app.utils.pyobjectid import PyObjectId


class CreateCredentialReqDto(BaseModel):
    name: str
    description: Optional[str] = ""
    api_key: SecretStr
    metadata: Optional[dict] = {}


class CreateCredentialDto(CreateCredentialReqDto):
    user_id: Optional[PyObjectId] = None
    key: Optional[str] = None


class DeleteCredentialDto(BaseModel):
    user_id: PyObjectId
    user_role: UserRolesEnum
    credential_id: PyObjectId
