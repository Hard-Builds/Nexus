from fastapi import HTTPException

from app.dao.profile_dao import ProfileDAO
from app.database.schemas.profile import ProfileSchema
from app.dto.profile_dto import CreateProfileReqDto, UpdateProfileReqDto, \
    UpdateStatusProfileReqDto
from app.enums.http_config import HttpStatusCode
from app.enums.profile_enum import ProfileActiveStatusEnum
from app.middleware.context import RequestContext
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId


class ProfileService:
    def __init__(self):
        self.__profile_dao = ProfileDAO()

    def __profile_validations(self, profile_dtl: dict,
                              check_status=True) -> None:
        if not profile_dtl:
            raise HTTPException(
                status_code=HttpStatusCode.NOT_FOUND,
                detail="Profile Details Not Found!"
            )

        if profile_dtl.get(
                "created_on") != RequestContext.get_context_user_id():
            raise HTTPException(
                status_code=HttpStatusCode.BAD_REQUEST,
                detail="You cannot access this profile!"
            )

        if check_status and profile_dtl.get(
                "active_status") != ProfileActiveStatusEnum.ACTIVE:
            raise HTTPException(
                status_code=HttpStatusCode.BAD_REQUEST,
                detail="Profile is not ACTIVE!"
            )

    def add_profile_func(self, req_dto: CreateProfileReqDto) -> PyObjectId:
        try:
            profile_id: PyObjectId = self.__profile_dao.add_profile(req_dto)
            return profile_id
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def get_profile_func(self, profile_id: PyObjectId) -> dict:
        try:
            profile_dtl: dict = self.__profile_dao.get_profile(profile_id)
            self.__profile_validations(profile_dtl)
            return profile_dtl
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def update_profile_func(self, req_dto: UpdateProfileReqDto) -> None:
        try:
            profile_id = req_dto.profile_id
            _ = self.get_profile_func(profile_id)

            update_info: dict = ProfileSchema(**req_dto.dict()).dict(
                exclude_unset=True)
            _ = self.__profile_dao.update_profile(profile_id, update_info)
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def status_update_profile_func(
            self, req_dto: UpdateStatusProfileReqDto) -> None:
        try:
            profile_id: PyObjectId = req_dto.profile_id
            profile_dtl: dict = self.__profile_dao.get_profile(profile_id)
            self.__profile_validations(profile_dtl, check_status=False)

            if profile_dtl.get("active_status") == req_dto.active_status:
                raise HTTPException(
                    status_code=HttpStatusCode.BAD_REQUEST,
                    detail=f"Profile is already {req_dto.active_status}."
                )

            update_info: dict = ProfileSchema(**req_dto.dict()).dict(
                exclude_unset=True)
            self.__profile_dao.update_profile(profile_id, update_info)
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def delete_profile_func(self, profile_id: PyObjectId) -> None:
        try:
            _ = self.get_profile_func(profile_id)
            self.__profile_dao.delete_profile(profile_id)
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)
