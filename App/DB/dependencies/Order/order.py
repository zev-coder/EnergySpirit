from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal


class OrderBase(BaseModel):
    customer_email: str
    customer_name: str
    customer_phone: str

    address_detail: str
    village: str
    district: str
    city: str
    province: str
    postal_code: str | None = None

    delivery_note: str | None = None


class OrderUpdate(BaseModel):
    customer_email: str
    customer_name: str
    customer_phone: str

    address_detail: str
    village: str
    district: str
    city: str
    province: str
    postal_code: str | None = None

    delivery_note: str | None = None

    product_id: int


class OrderRead(OrderBase):
    id: int
    total_amount: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
