from typing import Any

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
