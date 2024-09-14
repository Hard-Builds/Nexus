from pydantic import BaseModel, SecretStr


class AddUserDto(BaseModel):
    name: str
    username: str
    password: SecretStr

class UserLoginDto(BaseModel):
    username: str
    password: SecretStr
