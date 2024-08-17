from typing import Optional

from pydantic import BaseModel


class CreateProfileReqDto(BaseModel):
    name: str
    description: Optional[str] = ""
    config: dict


