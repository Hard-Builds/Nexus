from fastapi import APIRouter
from fastapi import Request

from app.dto.app_dto import AddAppReqDto, KeyRotateAppDto, AppStatusUpdateDto
from app.enums.http_config import HttpStatusCode
from app.enums.user_enum import UserRolesEnum
from app.middleware.auth_middleware import UserValidator
from app.service.app_service import AppService
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId

app_api_router = APIRouter(prefix="/app", tags=["App management"])

app_service = AppService()


@app_api_router.put("/add")
@UserValidator.pre_authorizer(
    authorized_roles=[UserRolesEnum.ADMIN, UserRolesEnum.MEMBER])
def add_app_controller(request: Request, req_dto: AddAppReqDto) -> dict:
    try:
        app_id: PyObjectId = app_service.add_app(req_dto)
        return AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="App Added Successfully!",
            data=str(app_id)
        )
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@app_api_router.put("/rotate-key")
@UserValidator.pre_authorizer(authorized_roles=[UserRolesEnum.ADMIN])
def rotate_app_key_controller(request: Request,
                              req_dto: KeyRotateAppDto) -> dict:
    try:
        new_key: str = app_service.rotate_app_key(req_dto)
        return AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="App Key Updated Successfully!",
            data=str(new_key)
        )
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@app_api_router.put("/status/update")
@UserValidator.pre_authorizer(authorized_roles=[UserRolesEnum.ADMIN])
def update_app_status_controller(request: Request,
                                 req_dto: AppStatusUpdateDto) -> dict:
    try:
        app_service.update_app_status(req_dto)
        return AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="App Status Updated Successfully!"
        )
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@app_api_router.put("/delete")
@UserValidator.pre_authorizer(authorized_roles=[UserRolesEnum.ADMIN])
def delete_app_controller(request: Request, app_id: PyObjectId) -> dict:
    try:
        app_service.delete_app(app_id)
        return AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="App Status Updated Successfully!"
        )
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)
