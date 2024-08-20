from fastapi import APIRouter, Request

from app.dto.credential_dto import CreateCredentialDto, CreateCredentialReqDto, \
    DeleteCredentialDto
from app.enums.http_config import HttpStatusCode
from app.enums.user_enum import UserRolesEnum
from app.middleware.auth_middleware import UserValidator
from app.middleware.context import RequestContext
from app.service.credential_service import CredentialService
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId

credential_api_router = APIRouter(prefix="/credential",
                                  tags=["Credential management"])
credential_service = CredentialService()


@credential_api_router.put("/create")
@UserValidator.pre_authorizer(
    authorized_roles=[UserRolesEnum.ADMIN, UserRolesEnum.MEMBER])
def create_credential_controller(request: Request,
                                 req_base_dto: CreateCredentialReqDto) -> dict:
    try:
        req_dto = CreateCredentialDto(**req_base_dto.dict())
        req_dto.user_id = RequestContext.get_context_user_id()
        credential_key: str = credential_service.add_credential_func(req_dto)
        response = AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="Credential Added Successfully!",
            data=credential_key
        )
        return response
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@credential_api_router.delete("/delete")
@UserValidator.pre_authorizer(
    authorized_roles=[UserRolesEnum.ADMIN, UserRolesEnum.MEMBER])
def delete_credential_controller(request: Request,
                                 credential_id: PyObjectId) -> dict:
    try:
        req_dto: DeleteCredentialDto = DeleteCredentialDto(
            user_id=RequestContext.get_context_user_id(),
            user_role=RequestContext.get_context_var(key="user_role"),
            credential_id=credential_id
        )

        credential_service.delete_credential_func(req_dto)
        response = AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="Credential Deleted Successfully!",
            data=str(credential_id)
        )
        return response
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)
