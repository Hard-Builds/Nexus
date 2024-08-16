import os
from datetime import timedelta

from jose import jwt

from app.utils.DateUtils import DateUtils

JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]


class AuthTokenServices:
    @staticmethod
    def generate_token(data: dict,
                       expires_delta: timedelta = timedelta(hours=1)):
        data["exp"] = DateUtils.get_current_timestamp() + expires_delta
        encoded_jwt = jwt.encode(data, JWT_SECRET_KEY)
        return encoded_jwt

    @staticmethod
    def validate_token(jwt_token):
        return jwt.decode(jwt_token, JWT_SECRET_KEY)
