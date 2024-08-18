from typing import Optional

from pydantic import BaseModel


class AddAppReqDto(BaseModel):
    name: str
    logo: Optional[str] = ""


class AddAppDto(AddAppReqDto):
    service_key: Optional[str] = ""
