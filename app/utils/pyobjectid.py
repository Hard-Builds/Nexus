from typing import Any

from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue


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
