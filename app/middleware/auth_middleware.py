from functools import wraps

from fastapi import Request, HTTPException
from jose import ExpiredSignatureError

from app.dao.user_dao import UserDAO
from app.enums.http_config import HttpStatusCode
from app.enums.user import UserActiveStatusEnum
from app.middleware.context import RequestContext
from app.service.auth.token_service import AuthTokenServices


class UserValidator:
    @staticmethod
    def authorise(request: Request, authorized_roles: list):
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

            if user_dtl["active_status"] != UserActiveStatusEnum.ACTIVE:
                raise HTTPException(
                    status_code=HttpStatusCode.FORBIDDEN,
                    detail="Your account has been deactivated, please contact admin for further help."
                )

            if user_dtl["role"] not in authorized_roles:
                raise HTTPException(
                    status_code=HttpStatusCode.UNAUTHORIZED,
                    detail="Sorry, you can't access this functionality. Please check your group settings or contact support."
                )

            RequestContext.set_context_var(key="user_id",
                                           value=user_dtl["_id"])
            RequestContext.set_context_var(key="user_role",
                                           value=user_dtl["role"])

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=HttpStatusCode.UNAUTHORIZED,
                detail="Your session is expired. Please Sign in again."
            )

    @staticmethod
    def pre_authorizer(authorized_roles: list):
        def decorator(func):
            @wraps(func)
            def wrapper(request: Request, *args, **kwargs):
                UserValidator.authorise(request, authorized_roles)
                return func(request, *args, **kwargs)

            return wrapper

        return decorator
