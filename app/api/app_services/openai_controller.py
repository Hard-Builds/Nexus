from fastapi import Request, APIRouter

from app.dto.open_ai_dto import OpenAIChatReqDto
from app.enums.sys_enum import ServiceApiTagEnum
from app.middleware.auth_middleware import UserValidator
from app.service.app_services.open_ai_service import OpenAIService
from app.utils.app_utils import AppUtils

open_ai_service_router = APIRouter(prefix="/open-ai",
                                   tags=[ServiceApiTagEnum.OPENAI])


@open_ai_service_router.put("/completion")
@UserValidator.pre_authorizer(support_app_key=True)
def open_ai_chat_controller(request: Request, req_dto: OpenAIChatReqDto):
    try:
        open_api_service = OpenAIService()
        return open_api_service.completion_func(req_dto)
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)
