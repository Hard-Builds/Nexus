from fastapi import HTTPException

from app.dao.credential_dao import CredentialDAO
from app.dao.profile_dao import ProfileDAO
from app.database.pipeline_builder import MongoPipelineBuilder
from app.dto.credential_dto import CreateCredentialDto, DeleteCredentialDto
from app.enums.http_config import HttpStatusCode
from app.enums.user_enum import UserRolesEnum
from app.middleware.context import RequestContext
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId


class CredentialService:
    def __init__(self):
        self.__profile_dao = ProfileDAO()
        self.__credential_dao = CredentialDAO()

    def add_credential_func(self, req_dto: CreateCredentialDto) -> PyObjectId:
        try:
            credential_id = self.__credential_dao.add_credential(req_dto)
            return credential_id
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def delete_credential_func(self, req_dto: DeleteCredentialDto) -> None:
        try:
            credential_id = req_dto.credential_id

            cred_dtl: dict = self.__credential_dao.get_credential_dtl_by_id(
                credential_id)
            if not cred_dtl:
                raise HTTPException(
                    status_code=HttpStatusCode.NOT_FOUND,
                    detail="Credential details not found for provided key!"
                )

            if cred_dtl.get("created_by") != req_dto.user_id and \
                    req_dto.user_role != UserRolesEnum.ADMIN:
                raise HTTPException(
                    status_code=HttpStatusCode.UNAUTHORIZED,
                    detail="You are not allowed to perform this action. Please contact admin."
                )

            self.__check_cred_utility(cred_dtl['api_key'])
            self.__credential_dao.delete_by_id(credential_id)

        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def __check_cred_utility(self, api_key: str):
        user_id: PyObjectId = RequestContext.get_context_user_id()
        user_id: PyObjectId = AppUtils.bson_objectId_converter(user_id)

        pipeline: list = [
            MongoPipelineBuilder.match_operator({
                "is_deleted": False,
                "created_by": user_id
            }),
            MongoPipelineBuilder.project_operator({
                "targets": "$config.targets"
            }),
            MongoPipelineBuilder.unwind_operator(path="$targets"),
            MongoPipelineBuilder.match_operator({
                "targets.virtual_key": api_key
            }),
            MongoPipelineBuilder.count_operator(key_name="total")
        ]
        result_list: list = self.__profile_dao.profile_pipeline_aggregation(
            pipeline)

        if result_list:
            raise HTTPException(
                status_code=HttpStatusCode.BAD_REQUEST,
                detail=f"virtual_key: {api_key} is in use!"
            )
