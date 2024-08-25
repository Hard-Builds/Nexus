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

    def add_credential_func(self, req_dto: CreateCredentialDto) -> str:
        try:
            req_dto.key = self.__gen_credential_key(req_dto.name)
            _ = self.__credential_dao.add_credential(req_dto)
            credential_key = req_dto.key
            return credential_key
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

    def __gen_credential_key(self, name: str) -> str:
        if len(name) > 5:
            name = name[:5]
        name: str = AppUtils.convert_special_chars_to_underscore(name)
        random_string: str = AppUtils.get_random_str(length=7)

        service_key: str = f"{name}-{random_string}"
        return service_key

    def get_credential_dtl_by_key(self, service_key: str) -> dict:
        search_by: dict = {"key": service_key, "is_deleted": False}
        cred_dtl: dict = self.__credential_dao.get_cred_dtls(search_by)

        if not cred_dtl:
            raise HTTPException(
                status_code=HttpStatusCode.BAD_REQUEST,
                detail="Key not found!"
            )
        return cred_dtl
