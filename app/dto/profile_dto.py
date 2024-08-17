from typing import Optional

from pydantic import BaseModel

from app.utils.pyobjectid import PyObjectId


class CreateProfileReqDto(BaseModel):
    name: str
    description: Optional[str] = ""
    config: dict


class CreateProfileDto(CreateProfileReqDto):
    user_id: Optional[PyObjectId] = None
