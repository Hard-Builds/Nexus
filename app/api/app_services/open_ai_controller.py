from fastapi import APIRouter, Request

from app.dto.app_services_dto.open_ai_dto import OpenAIChatCompletion
from app.enums.http_config import HttpStatusCode
from app.enums.user_enum import UserRolesEnum
from app.middleware.auth_middleware import UserValidator
from app.service.app_services.open_ai_service import OpenAIServices
from app.utils.app_utils import AppUtils

open_ai_router = APIRouter(prefix="/open_ai", tags=["Open AI Service"])

openai_services = OpenAIServices()


@open_ai_router.get("")
@UserValidator.pre_authorizer(authorized_roles=[UserRolesEnum.MEMBER])
def chat_completion_controller(request: Request,
                               req_dto: OpenAIChatCompletion):
    try:
        openai_services.chat_completion_func(req_dto)
        response = AppUtils.response(
            status_code=HttpStatusCode.OK,
            message=""
        )
        return response
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)
