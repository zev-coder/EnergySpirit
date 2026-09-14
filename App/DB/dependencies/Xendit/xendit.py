from typing import Any, Literal
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

class CreateXenditPayment(BaseModel):
    """Body yang dikirim frontend untuk memulai pembayaran order."""

    order_id: UUID
    channel_code: str = Field(min_length=1)
    channel_properties: dict[str, Any] = Field(default_factory=dict)
    description: str | None = Field(default=None, max_length=255)
    metadata: dict[str, Any] = Field(default_factory=dict)


class XenditCreatePaymentRequest(BaseModel):
    """Payload yang diteruskan backend ke Xendit Payment Request API."""

    reference_id: str = Field(min_length=1, max_length=255)
    type: Literal["PAY"] = "PAY"
    country: str = Field(default="ID", pattern=r"^[A-Z]{2}$")
    currency: str = Field(default="IDR", pattern=r"^[A-Z]{3}$")
    request_amount: int = Field(gt=0)
    capture_method: Literal["AUTOMATIC"] = "AUTOMATIC"
    channel_code: str
    channel_properties: dict[str, Any]
    description: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class XenditPaymentResponse(BaseModel):
    """Respons payment request dari Xendit."""

    business_id: str | None = None
    reference_id: str
    payment_request_id: str
    payment_token_id: str | None = None
    customer_id: str | None = None
    latest_payment_id: str | None = None
    latest_payment: dict[str, Any] | None = None
    type: str
    country: str
    currency: str
    request_amount: int
    capture_method: str
    channel_code: str
    channel_properties: dict[str, Any] = Field(default_factory=dict)
    actions: list[dict[str, Any]] = Field(default_factory=list)
    status: str
    failure_code: str | None = None
    description: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created: datetime
    updated: datetime
