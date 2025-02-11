import json
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
import pytest
from app.database import (
    Base,
    engine_null_pool,
    async_session_maker_null_pool,
)
from app.models import *  # flake8: ignore
from app.main import app
from app.schemas.hotels import HotelIn
from app.schemas.rooms import RoomIn
from app.utils.db_manager import DBManager


@pytest.fixture(scope="session")
async def setup_db():
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open(
        "tests/json_fixtures/hotels.json", encoding="utf-8"
    ) as hotels_json:
        hotels = json.load(hotels_json)
    with open(
        "tests/json_fixtures/rooms.json", encoding="utf-8"
    ) as rooms_json:
        rooms = json.load(rooms_json)

    hotels = [HotelIn.model_validate(hotel) for hotel in hotels]
    rooms = [RoomIn.model_validate(room) for room in rooms]

    async with DBManager(
        session_factory=async_session_maker_null_pool
    ) as db:
        await db.hotels.add_batch(hotels)
        await db.rooms.add_batch(rooms)
        await db.commit()


@pytest.fixture(scope="module")
async def api_client() -> AsyncGenerator:
    """Фикстура асинхронного клиента FastAPI"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as fast_client:
        yield fast_client
