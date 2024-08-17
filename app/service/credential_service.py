from fastapi import HTTPException

from app.dao.credential_dao import CredentialDAO
from app.dto.credential_dto import CreateCredentialDto, DeleteCredentialDto
from app.enums.http_config import HttpStatusCode
from app.enums.user_enum import UserRolesEnum
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId


class CredentialService:
    def __init__(self):
        self.__credential_dao = CredentialDAO()

    def add_credential_func(self, req_dto: CreateCredentialDto) -> PyObjectId:
        try:
            credential_id = self.__credential_dao.add_credential(req_dto)
            return credential_id
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    # TODO: Check if the cred is attached to a config
    def delete_credential_func(self, req_dto: DeleteCredentialDto) -> None:
        try:
            credential_id = req_dto.credential_id

            cred_dtl: dict = self.__credential_dao.get_credential_dtl(
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

            self.__credential_dao.delete_by_id(credential_id)

        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)
