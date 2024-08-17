from fastapi import APIRouter, Request

from app.dto.profile_dto import CreateProfileReqDto, CreateProfileDto
from app.enums.http_config import HttpStatusCode
from app.enums.user_enum import UserRolesEnum
from app.middleware.auth_middleware import UserValidator
from app.middleware.context import RequestContext
from app.service.profile_service import ProfileService
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId

profile_api_router = APIRouter(prefix="/profile",
                               tags=["Profile management"])
profile_service = ProfileService()


@profile_api_router.put("/create")
@UserValidator.pre_authorizer(
    authorized_roles=[UserRolesEnum.ADMIN, UserRolesEnum.MEMBER])
def create_profile_controller(request: Request,
                              req_base_dto: CreateProfileReqDto) -> dict:
    try:
        req_dto = CreateProfileDto(**req_base_dto.dict())
        req_dto.user_id = RequestContext.get_context_user_id()
        credential_id: PyObjectId = profile_service.add_profile_func(
            req_dto)
        response = AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="Profile Added Successfully!",
            data=str(credential_id)
        )
        return response
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)
