import random
from typing import Union

from starlette.responses import JSONResponse

from app.client.openai_client import OpenAIClient
from app.dto.open_ai_dto import OpenAIChatReqDto
from app.middleware.context import RequestContext
from app.service.credential_service import CredentialService
from app.service.profile_service import ProfileService
from app.utils.pyobjectid import PyObjectId


class OpenAIService:
    def __init__(self):
        self.__profile_service = ProfileService()
        self.__credential_service = CredentialService()

    def completion_func(self, req_dto: OpenAIChatReqDto):
        """Get Profile details"""
        profile_id: PyObjectId = RequestContext.get_context_var("profile_id")
        profile_dtl: dict = self.__profile_service.get_profile_func(profile_id)

        """Weighted Round robin for load balancing of the keys"""
        config_json: dict = profile_dtl.get("config", {})
        targets: list = config_json.get("targets", [])

        virtual_key_dtl: dict = self.__get_virtual_key(targets)
        cred_virtual_key: str = virtual_key_dtl.get("virtual_key")

        cred_dtls: dict = self.__credential_service.get_credential_dtl_by_key(
            service_key=cred_virtual_key)
        api_key: str = cred_dtls.get("api_key")
        retry_dtl: dict = virtual_key_dtl.get("retry")

        fallback_dtl: dict = config_json.get("fallback")
        if fallback_dtl:
            fallback_virtual_key: str = fallback_dtl.get("virtual_key")
            fallback_cred_dtls: dict = self.__credential_service.get_credential_dtl_by_key(
                service_key=fallback_virtual_key)
            fallback_api_key: str = fallback_cred_dtls.get("api_key")
        else:
            fallback_api_key: str = ""

        """Invoking openai sdk with exp backoff"""
        openai_client = OpenAIClient(
            api_key=api_key,
            max_retries=retry_dtl.get("attempts"),
            on_status_codes=retry_dtl.get("onStatusCodes"),
            fallback_api_key=fallback_api_key,
            virtual_key=cred_virtual_key,
            fallback_virtual_key=fallback_virtual_key
        )
        status_code, client_response, headers = openai_client.complete(req_dto)

        # TODO: Appending log file

        response = JSONResponse(
            status_code=status_code,
            headers=headers,
            content=client_response.dict()
        )
        return response

    def __get_virtual_key(self, targets: list) -> Union[dict, None]:

        virtual_keys: list = [item["virtual_key"] for item in targets]
        weights: list = [item["weight"] for item in targets]

        chosen_virtual_key: str = random.choices(
            virtual_keys, weights=weights, k=1)[0]

        for item in targets:
            if item["virtual_key"] == chosen_virtual_key:
                return item
