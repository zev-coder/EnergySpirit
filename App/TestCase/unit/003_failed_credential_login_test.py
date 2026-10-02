import pytest
from httpx import AsyncClient
from App.TestCase.conftest import create_test_user

@pytest.mark.asyncio
async def test_failed_credential(client: AsyncClient):
    """ melakukan testinng jika credensial yang dimasukkan tidak benar """
    await create_test_user(client)

    login_data = {
        "username" : "failed",
        "email" : "failed@gmail.com",
        "password" : "test"
    }

    response = await client.post("/auth/jwt/login", data=login_data)

    assert response.status_code == 400
    assert "access_token" not in response.json()
