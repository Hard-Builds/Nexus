import time
from functools import wraps

from fastapi import Request, HTTPException
from jose import ExpiredSignatureError

from app.dao.user_dao import UserDAO
from app.database.models.user import User
from app.enums.http_config import HttpStatusCode
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
            user_dtl: User = user_dao.get_user_dtl(filters=[
                User.username == username,
                User.is_deleted == False
            ])
            if user_dtl.role not in authorized_roles:
                raise HTTPException(
                    status_code=HttpStatusCode.UNAUTHORIZED,
                    detail="Sorry, you can't access this functionality. Please check your group settings or contact support."
                )
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
