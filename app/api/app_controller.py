from fastapi import APIRouter

from app.dto.app_dto import AddAppDto, AddAppReqDto
from app.enums.http_config import HttpStatusCode
from app.service.app_service import AppService
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId

app_api_router = APIRouter(prefix="/app", tags=["App management"])

app_service = AppService()


@app_api_router.put("/add")
def add_app_controller(req_dto: AddAppReqDto) -> dict:
    try:
        app_id: PyObjectId = app_service.add_app(req_dto)
        return AppUtils.response(
            status_code=HttpStatusCode.OK,
            message="App Added Successfully!",
            data=str(app_id)
        )
    except Exception as exc:
        AppUtils.handle_exception(exc, is_raise=True)
