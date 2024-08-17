from fastapi import APIRouter, Request

from app.dto.profile_dto import CreateProfileReqDto, UpdateProfileReqDto, \
    UpdateStatusProfileReqDto
from app.enums.http_config import HttpStatusCode
from app.enums.user_enum import UserRolesEnum
from app.middleware.auth_middleware import UserValidator
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
                              req_dto: CreateProfileReqDto) -> dict:
    try:
        profile_id: PyObjectId = profile_service.add_profile_func(req_dto)
        response = AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="Profile Added Successfully!",
            data=str(profile_id)
        )
        return response
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@profile_api_router.get("/")
@UserValidator.pre_authorizer(
    authorized_roles=[UserRolesEnum.ADMIN, UserRolesEnum.MEMBER])
def get_profile_controller(request: Request,
                           profile_id: PyObjectId) -> dict:
    try:
        profile_dtl: dict = profile_service.get_profile_func(
            profile_id)
        response = AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="Profile Added Successfully!",
            data=profile_dtl
        )
        return response
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@profile_api_router.post("/update")
@UserValidator.pre_authorizer(
    authorized_roles=[UserRolesEnum.ADMIN, UserRolesEnum.MEMBER])
def update_profile_controller(request: Request,
                              req_dto: UpdateProfileReqDto) -> dict:
    try:
        profile_service.update_profile_func(req_dto)
        response = AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="Profile Updated Successfully!"
        )
        return response
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@profile_api_router.post("/status/update")
@UserValidator.pre_authorizer(
    authorized_roles=[UserRolesEnum.ADMIN, UserRolesEnum.MEMBER])
def status_update_profile_controller(request: Request,
                                     req_dto: UpdateStatusProfileReqDto) -> dict:
    try:
        profile_service.status_update_profile_func(req_dto)
        response = AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="Profile Status Updated Successfully!"
        )
        return response
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)


@profile_api_router.delete("/delete")
@UserValidator.pre_authorizer(
    authorized_roles=[UserRolesEnum.ADMIN, UserRolesEnum.MEMBER])
def delete_profile_controller(request: Request,
                              profile_id: PyObjectId) -> dict:
    try:
        profile_service.delete_profile_func(profile_id)
        response = AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="Profile Deleted Successfully!"
        )
        return response
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)
