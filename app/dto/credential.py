from typing import Optional

from pydantic import BaseModel

from app.database.schemas import PyObjectId


class CreateCredentialDto(BaseModel):
    user_id: Optional[PyObjectId] = None
    name: str
    description: Optional[str] = ""
    api_key: str
    metadata: Optional[dict] = {}
