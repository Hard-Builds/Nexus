from fastapi import APIRouter, Request

from app.database.schemas import PyObjectId
from app.dto.credential import CreateCredentialDto
from app.enums.http_config import HttpStatusCode
from app.enums.user import UserRolesEnum
from app.middleware.auth_middleware import UserValidator
from app.service.credential.credential_service import CredentialService
from app.utils.app_utils import AppUtils

credential_op_api_router = APIRouter()
credential_service = CredentialService()


@credential_op_api_router.put("/create")
@UserValidator.pre_authorizer(
    authorized_roles=[UserRolesEnum.ADMIN, UserRolesEnum.MEMBER])
def create_credential_controller(request: Request,
                                 req_dto: CreateCredentialDto) -> dict:
    try:
        req_dto.user_id = request.__getattribute__("user_id")
        credential_id: PyObjectId = credential_service.add_credential_func(
            req_dto)
        response = AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="Credential Added Successfully!",
            data=str(credential_id)
        )
        return response
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)
