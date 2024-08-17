from pydantic import BaseModel


class AddUserDto(BaseModel):
    name: str
    username: str
    password: str

class UserLoginDto(BaseModel):
    username: str
    password: str
