from typing import Optional

from pydantic import BaseModel

from app.enums.app_enum import AppActiveStatusEnum
from app.utils.pyobjectid import PyObjectId


class AddAppReqDto(BaseModel):
    name: str
    logo: Optional[str] = ""


class AddAppDto(AddAppReqDto):
    service_key: Optional[str] = ""


class KeyRotateAppDto(AddAppReqDto):
    app_id: PyObjectId


class AppStatusUpdateDto(AddAppReqDto):
    app_id: PyObjectId
    active_status: AppActiveStatusEnum
