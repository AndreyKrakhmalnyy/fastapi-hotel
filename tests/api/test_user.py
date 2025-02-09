from httpx import AsyncClient


async def test_add_user(api_client: AsyncClient):
    data = {"email": "test@email.ru", "password": "test password"}
    response = await api_client.post("/auth/register", json=data)

    assert response.status_code == 200, response.content
