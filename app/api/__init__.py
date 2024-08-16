from fastapi import APIRouter

from app.api.users import users_api_router

api_router = APIRouter()
api_router.include_router(users_api_router)
