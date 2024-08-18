import random
import re
import string
import sys
import traceback
from typing import Any

from bson import ObjectId
from fastapi import HTTPException

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

    @staticmethod
    def handle_exception(exception, is_raise=False):
        exc_type, _, tb = sys.exc_info()
        f = tb.tb_frame
        line_no, filename, function_name = \
            tb.tb_lineno, f.f_code.co_filename, f.f_code.co_name

        message = exception.detail if hasattr(exception, "detail") \
            else f"Exception type: {exc_type}, " \
                 f"Exception message: {exception.__str__()}, " \
                 f"Filename: {filename}, " \
                 f"Function name: {function_name} " \
                 f"Line number: {line_no}" \
                 f"\n exception stack : {traceback.format_exc()}"

        print(message)

        if is_raise:
            raise HTTPException(
                status_code=exception.status_code
                if hasattr(exception, "status_code")
                else HttpStatusCode.INTERNAL_SERVER_ERROR,
                detail=message)

    @staticmethod
    def convert_object_id_to_str(data):
        if isinstance(data, dict):
            return {k: AppUtils.convert_object_id_to_str(v) for k, v in
                    data.items()}
        elif isinstance(data, list):
            return [AppUtils.convert_object_id_to_str(item) for item in data]
        elif isinstance(data, ObjectId):
            return str(data)
        else:
            return data

    @staticmethod
    def convert_special_chars_to_underscore(input_str: str) -> str:
        return re.sub(r'\W+', '_', input_str)

    @staticmethod
    def get_random_str(length: int) -> str:
        characters: str = string.ascii_letters + string.digits
        random_string: str = "".join(
            [random.choice(characters) for _ in range(length)])
        return str(random_string)
