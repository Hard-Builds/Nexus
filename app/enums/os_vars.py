from app.enums import StrEnum


class OSVarsEnum(StrEnum):
    DB_NAME = "DB_NAME"
    DATABASE_URL = "DATABASE_URL"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    ENV = "ENV"
    REDIS_HOST = "REDIS_HOST"
    REDIS_PORT = "REDIS_PORT"
