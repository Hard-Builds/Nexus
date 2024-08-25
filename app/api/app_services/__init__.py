from fastapi import APIRouter

from app.api.app_services.open_ai_controller import open_ai_router

app_services_router = APIRouter(prefix="/services")
app_services_router.include_router(open_ai_router)
