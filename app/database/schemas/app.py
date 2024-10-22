from typing import Optional

from app.database.schemas import PyDanticBaseModel
from app.enums.app_enum import AppActiveStatusEnum
from app.utils.pyobjectid import PyObjectId


class AppSchema(PyDanticBaseModel):
    name: str
    logo: Optional[str] = ""
    service_key: str
    active_status: Optional[
        AppActiveStatusEnum] = AppActiveStatusEnum.ACTIVE.value
    profile_id: Optional[PyObjectId] = None
