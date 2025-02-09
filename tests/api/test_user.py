from tests.conftest import api_client


async def test_add_user(api_client: api_client):
    data = {"email": "test email", "password": "test password"}
    await api_client.post("auth/register/", json=data)
