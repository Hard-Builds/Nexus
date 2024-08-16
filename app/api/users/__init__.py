from fastapi import APIRouter

from app.api.users.user_management import user_op_api_router

users_api_router = APIRouter(prefix="/users", tags=["User management"])
users_api_router.include_router(user_op_api_router)
