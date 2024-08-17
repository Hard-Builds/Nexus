from app.dao.profile_dao import ProfileDAO
from app.dto.profile_dto import CreateProfileDto
from app.utils.app_utils import AppUtils
from app.utils.pyobjectid import PyObjectId


class ProfileService:
    def __init__(self):
        self.__profile_dao = ProfileDAO()

    def add_profile_func(self, req_dto: CreateProfileDto) -> PyObjectId:
        try:
            profile_id: PyObjectId = self.__profile_dao.add_profile(req_dto)
            return profile_id
        except Exception as exc:
            AppUtils.handle_exception(exc, is_raise=True)
