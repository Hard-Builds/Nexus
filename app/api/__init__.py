from fastapi import APIRouter

from app.api.credential_controller import credential_api_router
from app.api.profile_controller import profile_api_router
from app.api.user_controller import users_api_router

api_router = APIRouter()
api_router.include_router(users_api_router)
api_router.include_router(credential_api_router)
api_router.include_router(profile_api_router)
