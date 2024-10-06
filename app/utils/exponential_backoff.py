import json
import time
from functools import wraps

from app.enums.http_config import HttpStatusCode
from app.utils.cryptography_utils import CryptographyUtils


class ExpBackoff:
    def __init__(self, api_key: str, fallback_api_key: str,
                 virtual_key: str, fallback_virtual_key: str,
                 max_retries: int = None,
                 on_status_codes: list[HttpStatusCode] = None):
        self.__max_retries: int = (max_retries or 0)
        self.__on_status_codes: list[HttpStatusCode] = (on_status_codes or [])
        self.__api_key = api_key
        self.__fallback_api_key = fallback_api_key
        self.__virtual_key = virtual_key
        self.__fallback_virtual_key = fallback_virtual_key

    def __call__(self, func):
        @wraps(func)
        def wrapper_func(*args, **kwargs):

            status_code: HttpStatusCode = HttpStatusCode.INTERNAL_SERVER_ERROR
            resp: dict = None

            time_map: list = []
            headers: dict = {
                "cache-hit": "false",
                "execution-key": "",
                "processing-time": "",
                "fallback-processing-time": ""
            }

            api_key = CryptographyUtils.decrypt(self.__api_key)

            for itr, attempt in enumerate(range(self.__max_retries)):

                start_time: time = time.time()
                status_code, resp = func(api_key=api_key, *args, **kwargs)
                time_taken: time = time.time() - start_time
                time_map.append("{:.2f}".format(time_taken))

                if status_code not in self.__on_status_codes:
                    headers["execution-key"] = self.__virtual_key
                    break
                elif attempt < self.__max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {status_code}.")

            if self.__fallback_api_key and status_code in self.__on_status_codes:
                print("Attempting Fallback...")

                fallback_api_key = CryptographyUtils.decrypt(
                    self.__fallback_api_key)
                start_time: time = time.time()
                status_code, resp = func(api_key=fallback_api_key,
                                         *args, **kwargs)
                if status_code == HttpStatusCode.OK:
                    headers["execution-key"] = self.__fallback_virtual_key
                time_taken: time = time.time() - start_time
                headers["fallback-processing-time"] = "{:.2f}".format(
                    time_taken)

            headers["processing-time"] = json.dumps(time_map)

            return status_code, resp, headers

        return wrapper_func
