"""Initialising context vars"""
from contextvars import ContextVar
from typing import Optional

from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId

context_var_registry = {
    "user_id": ContextVar("user_id", default=None),
    "user_role": ContextVar("user_role", default=None),
    "trace_id": ContextVar("trace_id", default=None)
}


class RequestContext:
    @staticmethod
    def get_context_var(key: str) -> str:
        return context_var_registry[key].get()

    @staticmethod
    def get_context_user_id() -> PyObjectId:
        user_id: str = RequestContext.get_context_var(key="user_id")
        user_id: PyObjectId = AppUtils.bson_objectId_converter(user_id)
        return user_id

    @staticmethod
    def set_context_var(key: str, value: Optional[str]) -> str:
        context_var_registry[key].set(value)
        return RequestContext.get_context_var(key)

    @staticmethod
    def clear_context_data():
        for key in context_var_registry:
            RequestContext.set_context_var(key=key, value=None)
