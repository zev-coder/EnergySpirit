from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from App.DB.model import Base, User
from collections.abc import AsyncGenerator
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import Depends
from fastapi_users import FastAPIUsers
import uuid
from App.config import get_settings
from App.DB.dependencies.Roles.roles import RolesCreate
from App.DB.model import Roles


settings = get_settings()

#IN THIS CASE WE ARE USING ASYNC METHOD TO MANTAIN THE SERVER RUNNING PARALEL WITH DATABASE

#database engine where all of the database begin

engine=  create_async_engine(
    settings.DATABASE_URL,
    # Connection pool configuration
    pool_size=settings.db_pool_size,           # Permanent connections in pool
    max_overflow=settings.db_max_overflow,     # Temporary connections during spikes
    pool_timeout=settings.db_pool_timeout,     # Wait time for connection
    pool_recycle=settings.db_pool_recycle,     # Prevent stale connections
    pool_pre_ping=True,                        # Verify connection before use

    # SQL logging for debugging
    echo=settings.db_echo,
)

#creating async engine
async_local_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=True,
    class_= AsyncSession
)

#creating a table when the server running
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_setup_role():
    async with async_local_session() as session:
        roles = {
            "MEMBER": RolesCreate(roles_name="MEMBER"),
            "MODERATOR": RolesCreate(roles_name="MODERATOR"),
        }
        for i in roles.values():
            role = Roles(**i.model_dump())
            session.add(role)
        await session.commit()


#giving a query to client
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_local_session() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
