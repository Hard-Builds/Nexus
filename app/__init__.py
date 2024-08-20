from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader

from core.api_settings import get_api_settings

API_KEY_NAME = "authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def common_headers(authorization: str = Security(api_key_header)):
    return {"authorization": authorization}


def get_app() -> FastAPI:
    get_api_settings.cache_clear()
    settings = get_api_settings()
    app = FastAPI(**settings.fastapi_kwargs)

    origins = [
        "*"
    ]

    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
    return app
