from typing import Optional

from pydantic import BaseModel

from app.utils.pyobjectid import PyObjectId
from app.enums.user_enum import UserRolesEnum


class CreateCredentialReqDto(BaseModel):
    name: str
    description: Optional[str] = ""
    api_key: str
    metadata: Optional[dict] = {}


class CreateCredentialDto(CreateCredentialReqDto):
    user_id: Optional[PyObjectId] = None


class DeleteCredentialDto(BaseModel):
    user_id: PyObjectId
    user_role: UserRolesEnum
    credential_id: PyObjectId
