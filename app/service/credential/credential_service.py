from app.dao.credential_dao import CredentialDAO
from app.database.schemas import PyObjectId
from app.dto.credential import CreateCredentialDto
from app.utils.app_utils import AppUtils


class CredentialService:
    def __init__(self):
        self.__credential_dao = CredentialDAO()

    def add_credential_func(self, req_dto: CreateCredentialDto) -> PyObjectId:
        try:
            credential_id = self.__credential_dao.add_credential(req_dto)
            return credential_id
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)
