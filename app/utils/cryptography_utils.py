import os

from cryptography.fernet import Fernet

from app.enums.os_vars import OSVarsEnum

THIRD_PARTY_SECRET_KEY = os.environ[OSVarsEnum.THIRD_PARTY_SECRET_KEY.value]


class CryptographyUtils:
    __fernet = Fernet(THIRD_PARTY_SECRET_KEY)

    @staticmethod
    def encrypt(val: str) -> bytes:
        return CryptographyUtils.__fernet.encrypt(val.encode())

    @staticmethod
    def decrypt(val: str | bytes) -> str:
        return CryptographyUtils.__fernet.decrypt(val).decode()
