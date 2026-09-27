from typing import Any, Literal
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr



class CreateXenditPayment(BaseModel):
    """Body yang dikirim frontend untuk memulai pembayaran order."""
    external_id: str = Field(max_length=255)
    amount_id: float
    payer_email: EmailStr
    description: str | None = Field(default=None, max_length=255)
    currency: str = Field(default="IDR", max_length=3)

class XenditPaymentResponses(BaseModel):
    """ Body yang akan diterima dari response api """
    uuid: UUID
    external_id: str = Field(max_length=255)
    amount_id: float
    payer_email: EmailStr
    description: str | None = Field(default=None, max_length=255)
    invoice_url: str
    status: str
    currency: str = Field(default="IDR", max_length=3)
