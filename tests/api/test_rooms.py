import json
import aiofiles
from pathlib import Path
from httpx import AsyncClient

FIXTURES_DIR = Path(__file__).parent.parent / "json_fixtures"
ROOMS_FIXTURE = FIXTURES_DIR / "rooms.json"


async def test_add_rooms(api_client: AsyncClient):
    async with aiofiles.open(ROOMS_FIXTURE, "r") as f:
        content = await f.read()
        rooms = json.loads(content)
        for room in rooms:
            response = await api_client.post(
                f"hotels/{room['hotel_id']}/rooms", json=room
            )

    assert response.status_code == 200, response.content
