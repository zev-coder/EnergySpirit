from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    roles_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    roles: Mapped[list['Roles']] = relationship(back_populates='users')
    created_product: Mapped[list['Product']] = relationship(back_populates='user')

class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)

    roles_name: Mapped[str] = mapped_column(
        String(59),
        unique=True,
        nullable=False
    )

    users: Mapped[list["User"]] = relationship(
        back_populates="roles"
    )

class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    created_by: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    users: Mapped[list['User']] = relationship(back_populates='product')

