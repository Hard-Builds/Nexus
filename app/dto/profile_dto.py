from typing import Optional

from pydantic import BaseModel

from app.enums.profile_enum import ProfileActiveStatusEnum
from app.utils.pyobjectid import PyObjectId


class CreateProfileReqDto(BaseModel):
    name: str
    description: Optional[str] = ""
    config: dict


class UpdateProfileReqDto(BaseModel):
    profile_id: PyObjectId
    name: Optional[str]
    description: Optional[str] = ""
    config: Optional[dict]


class UpdateStatusProfileReqDto(BaseModel):
    profile_id: PyObjectId
    active_status: ProfileActiveStatusEnum
