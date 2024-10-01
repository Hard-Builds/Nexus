import time
from functools import wraps

from app.enums.http_config import HttpStatusCode


class ExpBackoff:
    def __init__(self, api_key: str, fallback_api_key: str,
                 virtual_key: str, fallback_virtual_key: str,
                 max_retries: int = None,
                 on_status_codes: list[HttpStatusCode] = None,
                 initial_delay: int = None, multiplier: int = None):
        self.__max_retries: int = (max_retries or 0)
        self.__on_status_codes: list[HttpStatusCode] = (on_status_codes or [])
        self.__initial_delay: int = (initial_delay or 2)
        self.__multiplier: int = (multiplier or 2)
        self.__api_key = api_key
        self.__fallback_api_key = fallback_api_key
        self.__virtual_key = virtual_key
        self.__fallback_virtual_key = fallback_virtual_key

    def __call__(self, func):
        @wraps(func)
        def wrapper_func(*args, **kwargs):

            status_code: HttpStatusCode = HttpStatusCode.INTERNAL_SERVER_ERROR
            resp: dict = None
            headers: dict = {
                "accomplished-key": None
            }

            delay = self.__initial_delay
            for attempt in range(self.__max_retries):
                status_code, resp = func(self.__api_key, *args, **kwargs)

                if status_code not in self.__on_status_codes:
                    headers["accomplished-key"] = self.__virtual_key
                    break
                elif attempt < self.__max_retries - 1:
                    print(
                        f"Attempt {attempt + 1} failed: {status_code}. "
                        f"Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)
                    delay *= self.__multiplier

            if self.__fallback_api_key and not headers["accomplished-key"]:
                status_code, resp = func(self.__fallback_api_key, *args, **kwargs)
                if status_code == HttpStatusCode.OK:
                    headers["accomplished-key"] = self.__fallback_virtual_key

            return status_code, resp, headers

        return wrapper_func

