from fastapi import APIRouter

from app.api.credential.credential_controller import credential_op_api_router

credential_api_router = APIRouter(prefix="/credential",
                                  tags=["Credential management"])
credential_api_router.include_router(credential_op_api_router)
