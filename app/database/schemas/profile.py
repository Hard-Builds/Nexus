from typing import Optional, List

from pydantic import Field

from app.database.schemas import PyDanticBaseModel, CustomConfigBaseModel
from app.enums.credential_enum import CredentialProviderEnum
from app.enums.profile_enum import ProfileActiveStatusEnum, \
    ProfileStrategyModeEnum


class ProfileRetryModel(CustomConfigBaseModel):
    attempts: int
    onStatusCodes: List[int]


class ProfileTargetModel(CustomConfigBaseModel):
    provider: CredentialProviderEnum
    virtual_key: str
    weight: float = Field(ge=0, le=1)
    retry: ProfileRetryModel


class ProfileCacheModel(CustomConfigBaseModel):
    mode: str
    max_age: int


class ProfileStrategyModel(CustomConfigBaseModel):
    mode: ProfileStrategyModeEnum


class ProfileConfigModel(CustomConfigBaseModel):
    cache: Optional[ProfileCacheModel] = {}
    strategy: Optional[ProfileStrategyModel] = {}
    targets: Optional[List[ProfileTargetModel]] = {}


class ProfileSchema(PyDanticBaseModel):
    name: Optional[str] = ""
    description: Optional[str] = ""
    config: Optional[ProfileConfigModel] = {}
    active_status: Optional[
        ProfileActiveStatusEnum] = ProfileActiveStatusEnum.ACTIVE.value
