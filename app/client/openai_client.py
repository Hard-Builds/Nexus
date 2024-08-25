from fastapi import Response
from openai import OpenAI, OpenAIError

from app.dto.open_ai_dto import OpenAIChatReqDto
from app.enums.http_config import HttpStatusCode
from app.utils.exponential_backoff import ExpBackoff


class OpenAIClient:
    def __init__(self, api_key: str,
                 max_retries: int = None,
                 on_status_codes: list[HttpStatusCode] = None):
        self.__api_key = api_key
        self.__exp_backoff_utils = ExpBackoff(
            max_retries=max_retries,
            on_status_codes=on_status_codes
        )

    def complete(self, req_dto: OpenAIChatReqDto) -> \
            (HttpStatusCode, Response):
        @self.__exp_backoff_utils
        def _complete():
            try:
                client = OpenAI(api_key=self.__api_key)
                response = client.completions.create(**req_dto.dict())
                print(response.choices[0].message['content'])
                return HttpStatusCode.OK, response
            except OpenAIError as e:
                print(f"An error occurred: {e}")
                return e.status_code, {}

        return _complete()
