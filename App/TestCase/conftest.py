import pytest_asyncio
from sqlalchemy import select
from App.DB.model import Roles
from App.DB.dependencies.Roles.roles import RolesCreate
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from App.app import app
from App.DB.db import get_async_session
from App.DB.model import Base


TEST_BASE_URL = "postgresql+asyncpg://test:test@localhost:5433/myapp_test"
_test_user = None

bind_engine = create_async_engine(
    TEST_BASE_URL,
    echo=False
)

session_maker = async_sessionmaker(
    bind=bind_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Initialize test database."""

    async with bind_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with bind_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await bind_engine.dispose()


@pytest_asyncio.fixture
async def test_session():
    """Create a new database session for each test."""

    async with session_maker() as session:
        yield session

@pytest_asyncio.fixture(scope="session")
async def create_setup_role(setup_test_db):
    async with session_maker() as session:
        query = await session.execute(select(Roles))

        result = query.scalars().all()

        if result == []:
            roles = {
                "MEMBER": RolesCreate(roles_name="MEMBER"),
                "MODERATOR": RolesCreate(roles_name="MODERATOR"),
            }
            for i in roles.values():
                role = Roles(**i.model_dump())
                session.add(role)
            await session.commit()

@pytest_asyncio.fixture
async def client(test_session, create_setup_role):
    """Memberikan klien HTTPX yang dikonfigurasi untuk pengujian FastAPI dengan sesi database uji."""

    async def override_get_async_session():
        yield test_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()


async def create_test_user(
        client: AsyncClient,
        email: str = "string@gmail.com",
        password: str = "string",
        username: str = "string"
):
        global _test_user

        if _test_user is not None:
            return _test_user

        data = {
            "email": email,
            "username" : username,
            "password": password
        }

        response = await client.post("/auth/register", data=data)
        _test_user = response.json()

        print(f"Test user created: {response.json()}")
        assert response.status_code == 201, f"Failed to create test user: {response.text}"

        return _test_user


def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}

