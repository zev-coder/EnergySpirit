import stripe
from dotenv import load_dotenv
import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from App.DB.db import get_async_session
from App.DB.model import Product
from fastapi import Depends


client = stripe.StripeClient(os.environ['STRIPE_SECRET'])

async def create_session_checkout(price:int, quantity:int, id:int,session:AsyncSession = Depends(get_async_session)):
    query = session.execute(select(Product).where(Product.id  == id))

    if quantity:
        pass

    checkout_session = client.v1.checkout.sessions.create(
        params={
            'line_items' : [
                {
                    'price' : f'{price}'
                }
            ]
        }
    )
