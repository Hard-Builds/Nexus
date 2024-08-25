from fastapi import HTTPException

from app.dao.credential_dao import CredentialDAO
from app.dao.profile_dao import ProfileDAO
from app.database.schemas.profile import ProfileSchema, ProfileTargetModel
from app.dto.profile_dto import CreateProfileReqDto, UpdateProfileReqDto, \
    UpdateStatusProfileReqDto
from app.enums.credential_enum import CredentialProviderEnum
from app.enums.http_config import HttpStatusCode
from app.enums.profile_enum import ProfileActiveStatusEnum
from app.enums.user_enum import UserRolesEnum
from app.middleware.context import RequestContext
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId


class ProfileService:
    def __init__(self):
        self.__profile_dao = ProfileDAO()
        self.__credential_dao = CredentialDAO()

    def __profile_validations(self, profile_dtl: dict,
                              check_status=True) -> None:
        if not profile_dtl:
            raise HTTPException(
                status_code=HttpStatusCode.NOT_FOUND,
                detail="Profile Details Not Found!"
            )

        user_role: str = RequestContext.get_context_var("user_role")
        if user_role != UserRolesEnum.ADMIN or profile_dtl.get(
                "created_by") != RequestContext.get_context_user_id():
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
            self.__validate_profile_config(profile_config=req_dto.config)
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

            self.__validate_profile_config(profile_config=req_dto.config)

            update_info: dict = ProfileSchema(
                **req_dto.dict(exclude_none=True)).dict(exclude_unset=True)
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
                    detail=f"Profile is already {req_dto.active_status.value}."
                )

            update_info: dict = ProfileSchema(**req_dto.dict()).dict(
                exclude_unset=True)
            self.__profile_dao.update_profile(profile_id, update_info)
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def delete_profile_func(self, profile_id: PyObjectId) -> None:
        try:
            profile_dtl: dict = self.__profile_dao.get_profile(profile_id)
            self.__profile_validations(profile_dtl, check_status=False)
            self.__profile_dao.delete_profile(profile_id)
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def __validate_profile_config(self, profile_config: dict):
        profile_targets: list[ProfileTargetModel] = profile_config.get(
            "targets", [])
        for profile_target in profile_targets:
            self.__validate_profile_target(profile_target)

    def __validate_profile_target(self, profile_target: ProfileTargetModel):
        virtual_key: str = profile_target.get("virtual_key")
        provider: CredentialProviderEnum = profile_target.get("provider")

        search_by = {
            "key": virtual_key,
            "provider": provider,
            "is_deleted": False
        }
        credential_dtl: dict = self.__credential_dao.get_first_credential_dtl(
            search_by=search_by)

        if not credential_dtl:
            raise HTTPException(
                status_code=HttpStatusCode.NOT_FOUND,
                detail=f"Invalid key: {virtual_key}"
            )

        if RequestContext.get_context_var(
                key="user_role") != UserRolesEnum.ADMIN \
                and credential_dtl.get(
            "created_by") != RequestContext.get_context_user_id():
            raise HTTPException(
                status_code=HttpStatusCode.UNAUTHORIZED,
                detail=f"You are not accessible to fetch {virtual_key} key."
            )
