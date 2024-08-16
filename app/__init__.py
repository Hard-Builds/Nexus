from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.api_settings import get_api_settings


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
