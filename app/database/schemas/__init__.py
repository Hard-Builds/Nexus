from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel

from app.utils.DateUtils import DateUtils


class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return v


class PyDanticBaseModel(BaseModel):
    is_deleted: bool = False
    created_on: datetime = DateUtils.get_current_epoch()
    modified_on: datetime = DateUtils.get_current_epoch()

    class Config:
        orm_mode = True
        use_enum_values = True
