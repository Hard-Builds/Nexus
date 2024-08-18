from app.dao.app_dao import AppDao
from app.dto.app_dto import AddAppDto, AddAppReqDto
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
            model.service_key = self.__generate_service_key(req_dto)
            app_id: PyObjectId = self.__app_dao.add_user(model=model)
            return app_id
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)

    def __generate_service_key(self, req_dto: AddAppReqDto) -> str:
        app_name: str = req_dto.name
        app_name: str = AppUtils.convert_object_id_to_str(app_name)
        if len(app_name) > 5:
            app_name = app_name[:5]

        user_id: PyObjectId = RequestContext.get_context_user_id()
        user_id: str = str(user_id)
        user_id: str = user_id[-5:]

        random_string: str = AppUtils.get_random_str(length=7)

        service_key: str = f"NEXUS-{app_name}-{user_id}-{random_string}"
        return service_key
