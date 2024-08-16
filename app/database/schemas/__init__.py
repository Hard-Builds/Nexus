from datetime import datetime

from pydantic import BaseModel

from app.utils.DateUtils import DateUtils


class PyDanticBaseModel(BaseModel):
    is_deleted: bool = False
    created_on: datetime = DateUtils.get_current_timestamp()
    modified_on: datetime = DateUtils.get_current_timestamp()

    class Config:
        orm_mode = True
        use_enum_values = True
