import base64
from uuid import uuid4
import requests
from App.config import get_settings
from App.DB.dependencies.Xendit.xendit import (
    XenditCreatePaymentRequest,
    XenditPaymentResponse,
)


def create_payment(
    country: str,
    currency: str,
    card_number: str,
    cvn: str,
    expiry_year: str,
    expiry_month: str,
    cardholder_first_name: str,
    cardholder_last_name: str,
    cardholder_email: str,
    cardholder_phone_number: str,
    description: str,
    request_amount: int,
    *,
    reference_id: str | None = None,
    metadata: dict[str, str] | None = None,
) -> XenditPaymentResponse:
    """Validasi data kartu, membuat payload Xendit, lalu mengirim payment request."""

    card_number = card_number.replace(" ", "").replace("-", "")
    if not card_number.isdigit() or not 12 <= len(card_number) <= 19:
        raise ValueError("Nomor kartu tidak valid")
    if not cvn.isdigit() or len(cvn) not in (3, 4):
        raise ValueError("CVN harus terdiri dari 3 atau 4 digit")
    if not expiry_year.isdigit() or len(expiry_year) != 4:
        raise ValueError("Tahun kadaluarsa harus 4 digit")
    if not expiry_month.isdigit() or not 1 <= int(expiry_month) <= 12:
        raise ValueError("Bulan kadaluarsa harus antara 1 dan 12")

    payload = XenditCreatePaymentRequest(
        reference_id=reference_id or f"PAYMENT-{uuid4()}",
        country=country.upper(),
        currency=currency.upper(),
        request_amount=request_amount,
        channel_code="CARDS",
        channel_properties={
            "mid_label": "CTV_TEST",
            "card_details": {
                "card_number": card_number,
                "cvn": cvn,
                "expiry_year": expiry_year,
                "expiry_month": expiry_month,
                "cardholder_first_name": cardholder_first_name,
                "cardholder_last_name": cardholder_last_name,
                "cardholder_email": cardholder_email,
                "cardholder_phone_number": cardholder_phone_number,
            },
            "skip_three_ds": False,
            "failure_return_url": "https://xendit.co/failure",
            "success_return_url": "https://xendit.co/success",
        },
        description=description,
        metadata=metadata or {},
    )

    api_key = get_settings().XENDIT_SECRET_API
    if not api_key:
        raise ValueError("XENDIT_SECRET_API belum diatur")
    encoded_key = base64.b64encode(f"{api_key}:".encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_key}",
        "Content-Type": "application/json",
        "api-version": "2024-11-11",
    }

    response = requests.post(
        "https://api.xendit.co/v3/payment_requests",
        headers=headers,
        json=payload.model_dump(exclude_none=True),
        timeout=15,
    )
    response.raise_for_status()
    return XenditPaymentResponse.model_validate(response.json())
