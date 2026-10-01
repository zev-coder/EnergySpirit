import pytest
from httpx import AsyncClient, ASGITransport
from App.TestCase.conftest import create_test_user, create_setup_role


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """ melakukan register user baru dengan tahap pengembangan """
    await create_test_user(client)

    login_data = {
        "username": "string",
        "password": "string",
        "email" : "string@gmail.com"
    }

    response = await client.post("/auth/jwt/login", data=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

