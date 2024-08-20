from typing import Optional

from app.database.schemas import PyDanticBaseModel, PyObjectId
from app.enums.credential_enum import CredentialProviderEnum


class CredentialSchema(PyDanticBaseModel):
    name: str
    description: Optional[str] = ""
    provider: Optional[CredentialProviderEnum] = CredentialProviderEnum.OPEN_AI.value
    api_key: str
    metadata: Optional[dict] = {}
    key: str
