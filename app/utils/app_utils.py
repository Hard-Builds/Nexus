from typing import Any

from bson import ObjectId

from app.enums.http_config import HttpStatusCode


class AppUtils:
    @staticmethod
    def response(status_code: HttpStatusCode, message: str,
                 data: Any = None) -> dict:
        return {
            "status_code": status_code,
            "message": message,
            "data": data
        }

    @staticmethod
    def bson_objectId_converter(val):
        if isinstance(val, ObjectId):
            return val
        if (val is not None) and (len(val) == 24):
            val = ObjectId(val)
        return val
