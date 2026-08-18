from pydantic import BaseModel
from pydantic import ConfigDict

class RolesCreate(BaseModel):
    roles_name: str

class RolesResponse(BaseModel):
    id: int
    roles_name: str

    model_config = ConfigDict(from_attributes=True)
