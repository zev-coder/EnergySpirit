from pydantic import BaseModel

class CreateProduct(BaseModel):
    name: str
    description:str
    created_by: str


class ProductResponses(BaseModel):
    name: str
    description:str
    created_by: str
