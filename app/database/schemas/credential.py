from typing import Optional

from app.database.schemas import PyDanticBaseModel, PyObjectId
from app.enums.credential import CredentialProviderEnum


class CredentialSchema(PyDanticBaseModel):
    user_id: PyObjectId
    name: str
    description: Optional[str] = ""
    provider: Optional[CredentialProviderEnum] = CredentialProviderEnum.OPEN_AI
    api_key: str
    metadata: Optional[dict] = {}
