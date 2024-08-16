from fastapi import APIRouter, Request

from app.database.schemas import PyObjectId
from app.dto.user import AddUserDto, UserLoginDto
from app.enums.http_config import HttpStatusCode
from app.enums.user import UserRolesEnum
from app.middleware.auth_middleware import UserValidator
from app.service.users.user_management import UserManagementService
from app.utils.app_utils import AppUtils

user_op_api_router = APIRouter()

user_management_service = UserManagementService()


@user_op_api_router.get("/list")
def list_user_controller() -> dict:
    try:
        user_list: list = user_management_service.list_users()
        return AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="User Details Found Successfully!",
            data=user_list
        )
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@user_op_api_router.put("/add")
def add_user_controller(req_dto: AddUserDto) -> dict:
    try:
        user_id: PyObjectId = user_management_service.add_user(req_dto)
        return AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="User Added Successfully!",
            data=str(user_id)
        )
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@user_op_api_router.delete("/delete")
@UserValidator.pre_authorizer(authorized_roles=[UserRolesEnum.ADMIN])
def delete_user_controller(request: Request, user_id: PyObjectId) -> dict:
    try:
        user_management_service.delete_user(user_id)
        return AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="User Deleted Successfully!"
        )
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@user_op_api_router.post("/disable")
@UserValidator.pre_authorizer(authorized_roles=[UserRolesEnum.ADMIN])
def disable_user_controller(request: Request, user_id: PyObjectId) -> dict:
    try:
        user_management_service.disable_user(user_id)
        return AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="User Disabled Successfully!"
        )
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@user_op_api_router.get("/login")
def user_login_controller(username: str, password: str) -> dict:
    try:
        req_dto = UserLoginDto(
            username=username,
            password=password
        )
        jwt_token: str = user_management_service.user_login(req_dto)
        return AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="User Logged In Successfully!",
            data=jwt_token
        )
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)
