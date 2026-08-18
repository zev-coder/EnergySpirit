import uuid
from fastapi_users import schemas

class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str = " "
    role_id: int = 2
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str = " "

class UserUpdate(schemas.BaseUserUpdate):
    username:str
    pass
