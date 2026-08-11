from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from enum import Enum
from datetime import datetime


# The base of Blueprints
class Base(DeclarativeBase):
    pass

class Status(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DENIED = "denied"

# User table for auth
class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'Users'

    username: Mapped[str] = mapped_column(String(30), nullable=False)
    created_product: Mapped[list['Product']] = relationship(back_populates='users')
    carts: Mapped[list['Carts']] = relationship(back_populates='users')
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"),nullable=False)

    role: Mapped["Roles"] = relationship(back_populates="users")

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
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now)

    created_by: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    users: Mapped['User'] = relationship(back_populates='created_product')
    cartsitem: Mapped[list['Cartsitem']] = relationship(back_populates='product')


class Carts(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Enum] = mapped_column(SQLEnum(Status), nullable=False, default=Status.PENDING)

    users_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    users: Mapped[list['User']] = relationship(back_populates='carts')
    cartsitem: Mapped[list['Cartsitem']] = relationship(back_populates='carts')

class Cartsitem(Base):
    __tablename__ = "cartsitem"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    carts_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))

    product: Mapped['Product'] = relationship(back_populates='cartsitem')
    carts: Mapped['Carts'] = relationship(back_populates='cartsitem')
