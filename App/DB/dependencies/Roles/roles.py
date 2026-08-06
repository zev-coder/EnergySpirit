from pydantic import BaseModel

class RolesCreate(BaseModel):
    roles_name: str

class RolesResponse(BaseModel):
    id: int
    name: str
