from base64 import b64encode
from uuid import UUID, uuid4
from pydantic import EmailStr
import requests
from App.DB.model import Order
from App.config import get_settings
from App.DB.dependencies.Xendit.xendit import (
    CreateXenditPayment,
    XenditPaymentResponses
)
import random
import string
import os
from dotenv import load_dotenv
import uuid


load_dotenv()

chars = string.ascii_letters + string.digits
hasil = ''.join(random.choice(chars) for i in range(4))
auth_key = os.getenv('XENDIT_SECRET_API')

def create_invoice(product:str ,external_id: str, amount_id:float, payer_email:EmailStr, description:str,currency:str, order_id:UUID) -> XenditPaymentResponses:

    external_id = f"ORDER-{product.capitalize()}-{order_id}"
    model = CreateXenditPayment(
        external_id=external_id,
        amount_id=amount_id,
        payer_email=payer_email,
        description=description,
        currency= currency
    )


    headers = {
        "Authorization": f"Basic {b64encode(f'{auth_key}:'.encode()).decode()}",
    }

    response = requests.post(
        'https://api.xendit.co/v2/invoices',
        headers=headers,
        json=model.model_dump(),
        timeout=10
    )

    if response.status_code != 201 and response.status_code != 200:
        raise Exception(f"Failed to create invoice: {response.text}")

    data = response.json()

    return XenditPaymentResponses(
        uuid= order_id,
        external_id=data['external_id'],
        amount_id=data['amount_id'],
        payer_email=data['payer_email'],
        invoice_url= data['invoice_url'],
        status= data['status']
    )

