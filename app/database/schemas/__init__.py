from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel
from pydantic.json_schema import JsonSchemaValue

from app.utils.DateUtils import DateUtils


class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any, values: dict = None, config: Any = None,
                 field: Any = None):
        if not ObjectId.is_valid(value):
            raise ValueError('Invalid ObjectId')
        return value

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: JsonSchemaValue,
                                     handler: Any):
        return {
            "type": "string",
            "format": "objectid",
        }


class PyDanticBaseModel(BaseModel):
    is_deleted: Optional[bool] = False
    created_on: Optional[int] = DateUtils.get_current_epoch()
    modified_on: Optional[int] = DateUtils.get_current_epoch()

    class Config:
        orm_mode = True
        use_enum_values = True
