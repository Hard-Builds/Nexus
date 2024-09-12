from typing import Optional

from pydantic import Field

from app.database.schemas import PyDanticBaseModel
from app.enums.credential_enum import CredentialProviderEnum
from app.utils.cryptography_utils import CryptographyUtils


class CredentialSchema(PyDanticBaseModel):
    name: str
    description: Optional[str] = ""
    provider: Optional[
        CredentialProviderEnum] = CredentialProviderEnum.OPEN_AI.value
    api_key: str = Field(default_factory=CryptographyUtils.encrypt)
    metadata: Optional[dict] = {}
    key: str
