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
    customer_email: str | None = None
    customer_name: str | None = None
    customer_phone: str | None = None

    address_detail: str | None = None
    village: str | None = None
    district: str | None = None
    city: str | None = None
    province: str | None = None
    postal_code: str | None = None

    delivery_note: str | None = None

    status: str | None = None
    product_id: int


class OrderRead(OrderBase):
    id: int
    total_amount: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
