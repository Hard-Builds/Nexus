from typing import Optional

from pydantic import BaseModel, Field

from app.middleware.context import RequestContext
from app.utils.DateUtils import DateUtils
from app.utils.pyobjectid import PyObjectId


class PyDanticBaseModel(BaseModel):
    is_deleted: Optional[bool] = False
    created_on: Optional[int] = DateUtils.get_current_epoch()
    modified_on: Optional[int] = DateUtils.get_current_epoch()
    created_by: Optional[PyObjectId] = Field(
        default_factory=RequestContext.get_context_user_id)
    modified_by: Optional[PyObjectId] = Field(
        default_factory=RequestContext.get_context_user_id)

    class Config:
        from_attributes = True
        use_enum_values = True
