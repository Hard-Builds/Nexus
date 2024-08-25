from functools import wraps

from fastapi import Request, HTTPException
from jose import ExpiredSignatureError

from app.dao.app_dao import AppDao
from app.dao.user_dao import UserDAO
from app.enums.app_enum import AppActiveStatusEnum
from app.enums.http_config import HttpStatusCode
from app.enums.user_enum import UserActiveStatusEnum
from app.middleware.context import RequestContext
from app.service.token_service import AuthTokenServices
from app.utils.pyobjectid import PyObjectId


class UserValidator:
    @staticmethod
    def user_authorise(request: Request, authorized_roles: list):
        try:
            jwt_token = request.headers.get('authorization')
            if not jwt_token:
                raise HTTPException(
                    status_code=HttpStatusCode.UNAUTHORIZED,
                    detail="Token is missing."
                )

            data: dict = AuthTokenServices.validate_token(jwt_token=jwt_token)
            username = data.get("username")

            user_dao = UserDAO()
            user_dtl: dict = user_dao.get_user_dtl(filters={
                "username": username,
                "is_deleted": False
            })
            UserValidator.validate_user_dtls(user_dtl,
                                             authorized_roles=authorized_roles)

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=HttpStatusCode.UNAUTHORIZED,
                detail="Your session is expired. Please Sign in again."
            )

    @staticmethod
    def app_key_authorise(request: Request):
        app_key: str = request.headers.get("x-api-key")

        if not app_key:
            raise HTTPException(
                status_code=HttpStatusCode.UNAUTHORIZED,
                detail="App Key is missing."
            )

        app_dao: AppDao = AppDao()
        app_dtl: dict = app_dao.get_app_dtl_dict({
            "service_key": app_key,
            "is_deleted": False
        })

        if not app_dtl:
            raise HTTPException(
                status_code=HttpStatusCode.UNAUTHORIZED,
                detail="Invalid App Key!"
            )

        if app_dtl.get("active_status") != AppActiveStatusEnum.ACTIVE:
            raise HTTPException(
                status_code=HttpStatusCode.UNAUTHORIZED,
                detail="App Key is not active!"
            )

        RequestContext.set_context_var(key="profile_id",
                                       value=app_dtl.get("profile_id"))

        """Getting user details"""
        user_dao = UserDAO()
        user_id: PyObjectId = app_dtl.get("created_by")
        user_dtl: dict = user_dao.get_user_dtl_by_id(user_id)
        UserValidator.validate_user_dtls(user_dtl)

    @staticmethod
    def validate_user_dtls(user_dtl: dict, authorized_roles: list = None):
        if user_dtl["active_status"] != UserActiveStatusEnum.ACTIVE:
            raise HTTPException(
                status_code=HttpStatusCode.FORBIDDEN,
                detail="Your account has been deactivated, please contact admin for further help."
            )

        if authorized_roles is not None and user_dtl[
            "role"] not in authorized_roles:
            raise HTTPException(
                status_code=HttpStatusCode.UNAUTHORIZED,
                detail="Sorry, you can't access this functionality. Please check your group settings or contact support."
            )

        RequestContext.set_context_var(key="user_id",
                                       value=user_dtl["_id"])
        RequestContext.set_context_var(key="user_role",
                                       value=user_dtl["role"])

    @staticmethod
    def pre_authorizer(authorized_roles: list = None,
                       support_app_key: bool = None):
        def decorator(func):
            @wraps(func)
            def wrapper(request: Request, *args, **kwargs):
                if authorized_roles is not None:
                    UserValidator.user_authorise(request, authorized_roles)
                elif support_app_key is not None:
                    UserValidator.app_key_authorise(request)
                return func(request, *args, **kwargs)

            return wrapper

        return decorator
