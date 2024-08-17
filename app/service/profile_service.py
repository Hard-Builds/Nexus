from fastapi import HTTPException

from app.dao.profile_dao import ProfileDAO
from app.dto.profile_dto import CreateProfileReqDto
from app.enums.http_config import HttpStatusCode
from app.enums.profile_enum import ProfileActiveStatusEnum
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId


class ProfileService:
    def __init__(self):
        self.__profile_dao = ProfileDAO()

    def add_profile_func(self, req_dto: CreateProfileReqDto) -> PyObjectId:
        try:
            profile_id: PyObjectId = self.__profile_dao.add_profile(req_dto)
            return profile_id
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def get_profile_func(self, profile_id: PyObjectId) -> dict:
        try:
            profile_dtl: dict = self.__profile_dao.get_profile(profile_id)
            if not profile_dtl:
                raise HTTPException(
                    status_code=HttpStatusCode.NOT_FOUND,
                    detail="Profile Details Not Found!"
                )

            if profile_dtl.get(
                    "active_status") != ProfileActiveStatusEnum.ACTIVE:
                raise HTTPException(
                    status_code=HttpStatusCode.BAD_REQUEST,
                    detail="Profile is not ACTIVE!"
                )

            return profile_dtl
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)
