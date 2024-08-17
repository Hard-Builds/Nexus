from typing import Optional

from app.database.schemas import PyDanticBaseModel
from app.enums.profile_enum import ProfileActiveStatusEnum


class ProfileSchema(PyDanticBaseModel):
    name: Optional[str] = ""
    description: Optional[str] = ""
    config: Optional[dict] = {}
    active_status: Optional[
        ProfileActiveStatusEnum] = ProfileActiveStatusEnum.ACTIVE.value
