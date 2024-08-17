from typing import Optional

from app.database.schemas import PyDanticBaseModel, PyObjectId
from app.enums.profile_enum import ProfileActiveStatusEnum
from app.enums.user_enum import UserActiveStatusEnum


class ProfileSchema(PyDanticBaseModel):
    name: str
    description: Optional[str] = ""
    config: Optional[dict] = {}
    active_status: Optional[
        ProfileActiveStatusEnum] = UserActiveStatusEnum.ACTIVE.value
