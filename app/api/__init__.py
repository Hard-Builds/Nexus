from fastapi import APIRouter

from app.api.credential import credential_api_router
from app.api.users import users_api_router

api_router = APIRouter()
api_router.include_router(users_api_router)
api_router.include_router(credential_api_router)
