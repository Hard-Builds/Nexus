from fastapi import HTTPException

from app.dao.app_dao import AppDao
from app.dto.app_dto import AddAppDto, AddAppReqDto, KeyRotateAppDto, \
    AppStatusUpdateDto
from app.enums.app_enum import AppActiveStatusEnum
from app.enums.http_config import HttpStatusCode
from app.middleware.context import RequestContext
from app.service.user_service import UserManagementService
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId


class AppService:
    def __init__(self):
        self.__app_dao = AppDao()
        self.__user_management_service = UserManagementService()

    def add_app(self, req_dto: AddAppReqDto) -> PyObjectId:
        try:
            model: AddAppDto = AddAppDto(**req_dto.dict())
            model.service_key = self.__generate_service_key(
                app_name=req_dto.name)
            app_id: PyObjectId = self.__app_dao.add_user(model=model)
            return app_id
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def __generate_service_key(self, app_name: str) -> str:
        if len(app_name) > 5:
            app_name = app_name[:5]
        app_name: str = AppUtils.convert_special_chars_to_underscore(app_name)

        user_id: PyObjectId = RequestContext.get_context_user_id()
        user_id: str = str(user_id)
        user_id: str = user_id[-5:]

        random_string: str = AppUtils.get_random_str(length=7)

        service_key: str = f"NEXUS-{app_name}-{user_id}-{random_string}"
        return service_key

    def rotate_app_key(self, req_dto: KeyRotateAppDto) -> str:
        try:
            app_id: PyObjectId = req_dto.app_id
            app_dtl: dict = self.__app_dao.get_app_dtls(app_id)

            if not app_dtl:
                raise HTTPException(
                    status_code=HttpStatusCode.NOT_FOUND,
                    detail="App Details Not Found!"
                )

            if app_dtl["active_status"] != AppActiveStatusEnum.ACTIVE:
                raise HTTPException(
                    status_code=HttpStatusCode.BAD_REQUEST,
                    detail=f'App is in {app_dtl["active_status"]} status.'
                )

            new_key: str = self.__generate_service_key(
                app_name=app_dtl["name"])

            update_info: dict = {"service_key": new_key}
            self.__app_dao.update_app_by_id(app_id, update_info)
            return new_key
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def update_app_status(self, req_dto: AppStatusUpdateDto) -> None:
        try:
            app_id: PyObjectId = req_dto.app_id
            app_dtl: dict = self.__app_dao.get_app_dtls(app_id)

            if not app_dtl:
                raise HTTPException(
                    status_code=HttpStatusCode.NOT_FOUND,
                    detail="App Details Not Found!"
                )

            if app_dtl["active_status"] == req_dto.active_status:
                raise HTTPException(
                    status_code=HttpStatusCode.BAD_REQUEST,
                    detail=f'App is in already in {app_dtl["active_status"]} status.'
                )

            update_info: dict = {"active_status": req_dto.active_status}
            self.__app_dao.update_app_by_id(app_id, update_info)
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def delete_app(self, app_id: PyObjectId) -> None:
        try:
            app_dtl: dict = self.__app_dao.get_app_dtls(app_id)

            if not app_dtl:
                raise HTTPException(
                    status_code=HttpStatusCode.NOT_FOUND,
                    detail="App Details Not Found!"
                )

            update_info: dict = {"is_deleted": True}
            self.__app_dao.update_app_by_id(app_id, update_info)
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)
