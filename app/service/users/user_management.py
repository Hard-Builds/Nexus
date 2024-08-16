from fastapi import HTTPException

from app.dao.user_dao import UserDAO
from app.database.schemas import PyObjectId
from app.dto.user import AddUserDto, UserLoginDto
from app.enums.http_config import HttpStatusCode
from app.enums.user import UserActiveStatusEnum
from app.service.auth.token_service import AuthTokenServices
from app.utils.DateUtils import DateUtils
from app.utils.password_utils import PasswordUtils


class UserManagementService:
    def __init__(self):
        self.__user_dao = UserDAO()

    def list_users(self) -> list:
        user_list: list = self.__user_dao.get_all_users()
        return user_list

    def add_user(self, req_dto: AddUserDto) -> PyObjectId:
        user_id: PyObjectId = self.__user_dao.add_user(user_model=req_dto)
        return user_id

    def delete_user(self, user_id: PyObjectId) -> None:
        user_dtl: dict = self.__user_dao.get_user_dtl_by_id(user_id)
        if not user_dtl:
            raise HTTPException(
                status_code=HttpStatusCode.NOT_FOUND,
                detail="User Details not found!"
            )

        self.__user_dao.delete_user_by_id(user_id)

    def disable_user(self, user_id: PyObjectId) -> None:
        user_dtl: dict = self.__user_dao.get_user_dtl_by_id(user_id)
        if not user_dtl:
            raise HTTPException(
                status_code=HttpStatusCode.NOT_FOUND,
                detail="User Details not found!"
            )

        if user_dtl.get("ActiveStatus") == UserActiveStatusEnum.DISABLED:
            raise HTTPException(
                status_code=HttpStatusCode.BAD_REQUEST,
                detail="User is already DISABLED!"
            )

        self.__user_dao.update_user_dtl(
            user_id=user_id,
            update_info={
                "ActiveStatus": UserActiveStatusEnum.DISABLED.value,
                "modified_on": DateUtils.get_current_epoch()
            }
        )

    def user_login(self, req_dto: UserLoginDto) -> str:
        username = req_dto.username
        user_dtl: dict = self.__user_dao.get_user_dtl(filters={
            "username": username,
            "is_deleted": False
        })

        if not user_dtl:
            raise HTTPException(
                status_code=HttpStatusCode.NOT_FOUND,
                detail="User details not found!"
            )

        if user_dtl["ActiveStatus"] != UserActiveStatusEnum.ACTIVE.value:
            raise HTTPException(
                status_code=HttpStatusCode.BAD_REQUEST,
                detail="User is not Active!"
            )

        valid_pwd = PasswordUtils.verify_password(
            plain_password=req_dto.password,
            hashed_password=user_dtl["password"]
        )

        if not valid_pwd:
            raise HTTPException(
                status_code=HttpStatusCode.UNAUTHORIZED,
                detail="Invalid Password!"
            )

        jwt_token = AuthTokenServices.generate_token(
            data={"username": username})
        return jwt_token
