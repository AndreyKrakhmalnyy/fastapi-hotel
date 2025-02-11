import json
import aiofiles
from pathlib import Path
from tests.conftest import api_client


FIXTURES_DIR = Path(__file__).parent.parent / "json_fixtures"
HOTELS_FIXTURE = FIXTURES_DIR / "hotels.json"


async def test_add_hotels(api_client: api_client):
    async with aiofiles.open(HOTELS_FIXTURE, "r") as f:
        content = await f.read()
        hotels = json.loads(content)
        for hotel in hotels:
            response = await api_client.post("/hotels", json=hotel)

    assert response.status_code == 200, response.content
