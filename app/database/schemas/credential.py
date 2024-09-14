from typing import Optional

from pydantic import validator, SecretStr

from app.database.schemas import PyDanticBaseModel
from app.enums.credential_enum import CredentialProviderEnum
from app.utils.cryptography_utils import CryptographyUtils


class CredentialSchema(PyDanticBaseModel):
    name: str
    description: Optional[str] = ""
    provider: Optional[
        CredentialProviderEnum] = CredentialProviderEnum.OPEN_AI.value
    api_key: SecretStr
    metadata: Optional[dict] = {}
    key: str

    @validator("api_key")
    def encrypt_api_key(cls, val):
        return CryptographyUtils.encrypt(val.get_secret_value())