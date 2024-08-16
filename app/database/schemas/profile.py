from typing import Optional

from app.database.schemas import PyDanticBaseModel, PyObjectId


class ProfileSchema(PyDanticBaseModel):
    user_id: PyObjectId
    name: str
    description: Optional[str] = ""
    config: Optional[dict] = {}
