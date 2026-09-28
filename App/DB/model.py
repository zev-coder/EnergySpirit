import decimal
import uuid
from typing import Any
from pydantic import EmailStr
from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, JSON, String, Text,Numeric,UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from enum import Enum
from datetime import datetime


# The base of Blueprints
class Base(DeclarativeBase):
    pass

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DENIED = "denied"

class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    EXPIRED = "expired"


# User table for auth
class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'Users'

    username: Mapped[str] = mapped_column(String(30), nullable=False)
    created_product: Mapped[list['Product']] = relationship(back_populates='users')

    photo: Mapped[str] = mapped_column(String(255), nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"),nullable=False)

    role: Mapped["Roles"] = relationship(back_populates="users")
    order: Mapped['Order'] = relationship(back_populates="users")

# Roles and have relation with User table
class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)

    roles_name: Mapped[str] = mapped_column(
        String(59),
        unique=True,
        nullable=False
    )

    users: Mapped[list["User"]] = relationship(back_populates="role")


#Product table that contain any product item
class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(12,2), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    photo: Mapped[str] = mapped_column(String(255), nullable=True)

    created_by: Mapped[UUID] = mapped_column(ForeignKey("Users.id"))
    users: Mapped['User'] = relationship(back_populates='created_product')

    #order relationship
    order: Mapped[list['Order']] = relationship(back_populates='product')


#Order transaction
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, index=True, default=uuid.uuid4)

    # =========================
    # CUSTOMER
    # =========================

    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    customer_phone: Mapped[str] = mapped_column( String(20), nullable=False)

    # =========================
    # DELIVERY ADDRESS
    # =========================
    address_detail: Mapped[str] = mapped_column(Text, nullable=False)
    village: Mapped[str] = mapped_column(String(100), nullable=False)
    district: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    province: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    delivery_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    # =========================
    # TRANSACTION
    # =========================

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    total_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2),nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    users_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))

    product: Mapped['Product'] = relationship(back_populates='order')
    users: Mapped[list['User']] = relationship(back_populates='order')

    payment: Mapped[list["Payment"]] = relationship(back_populates="order", uselist=False)


#Xendit table
class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(String(255),primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
        unique=True
    )

    provider: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    provider_payment_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True
    )

    amount: Mapped[decimal.Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="IDR"
    )

    status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False
    )

    provider_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    order: Mapped[list["Order"]] = relationship(
        back_populates="payment"
    )


