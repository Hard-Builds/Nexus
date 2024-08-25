import time
from functools import wraps

from app.enums.http_config import HttpStatusCode


class ExpBackoff:
    def __init__(self, max_retries: int = None,
                 on_status_codes: list[HttpStatusCode] = None,
                 initial_delay: int = None, multiplier: int = None):
        self.__max_retries: int = (max_retries or 0)
        self.__on_status_codes: list[HttpStatusCode] = (on_status_codes or [])
        self.__initial_delay: int = (initial_delay or 2)
        self.__multiplier: int = (multiplier or 2)

    def __call__(self, func):
        @wraps(func)
        def wrapper_func(*args, **kwargs):
            delay = self.__initial_delay
            for attempt in range(self.__max_retries):
                status_code, resp = func(*args, **kwargs)
                if status_code not in self.__on_status_codes:
                    break
                else:
                    print(
                        f"Attempt {attempt + 1} failed: {status_code}. "
                        f"Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)
                    delay *= self.__multiplier
            return resp

        return wrapper_func