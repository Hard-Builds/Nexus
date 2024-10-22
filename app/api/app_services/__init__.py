from fastapi import APIRouter

from app.api.app_services.openai_controller import open_ai_service_router

app_services_router = APIRouter(prefix="/services")
app_services_router.include_router(open_ai_service_router)
