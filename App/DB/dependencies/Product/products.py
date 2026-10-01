import datetime
from decimal import Decimal
from fastapi import Depends
from pydantic import BaseModel, Field
from uuid import UUID
from App.DB.db import get_user_db

test = Depends(get_user_db)

class CreateProduct(BaseModel):
    name: str
    description:str
    price: Decimal = Field(gt=0)
    quantity: int = Field(default=1, ge=1)



class ProductResponses(BaseModel):
    name: str
    description:str
    created_by: UUID
    created_at: datetime.datetime
