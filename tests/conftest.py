import json
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import insert
from app.database import (
    Base,
    engine_null_pool,
    async_session_maker_null_pool,
)
from app.models import *  # noqa: F403
from app.main import app
from app.models.hotels import HotelsOrm
from app.models.rooms import RoomsOrm
from app.schemas.hotels import HotelIn
from app.schemas.rooms import RoomIn
from app.utils.db_manager import DBManager
from sqlalchemy.orm import Session


async def get_db_null_pool():
    async with DBManager(
        session_factory=async_session_maker_null_pool
    ) as db:
        yield db


@pytest.fixture(scope="function")
async def db_session():
    async for db in get_db_null_pool():
        yield db


@pytest.fixture(scope="session", autouse=True)
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


@pytest.fixture(scope="session")
async def api_client() -> AsyncGenerator:
    """Фикстура асинхронного клиента FastAPI"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as fast_client:
        yield fast_client


@pytest.fixture(scope="session", autouse=True)
async def register_user(api_client: api_client):
    await api_client.post(
        "/auth/register",
        json={"email": "kot@pes.com", "password": "1234"},
    )


@pytest.fixture(scope="session")
async def auth_api_client(
    register_user: register_user, api_client: api_client
):
    await api_client.post(
        "/auth/login",
        json={"email": "kot@pes.com", "password": "1234"},
    )
    assert api_client.cookies["access_token"]
    yield api_client


@pytest.fixture(scope="session")
async def hotel(db_session: Session) -> HotelsOrm:
    """Фикстура отеля"""
    res = db_session.execute(
        insert(HotelsOrm)
        .values(title="Test Title", location="Test Location")
        .returning(HotelsOrm)
    ).scalar_one()
    db_session.commit()
    return res


@pytest.fixture(scope="session")
async def room(db_session: Session, hotel: hotel) -> RoomsOrm:
    """Фикстура комнаты"""
    res = db_session.execute(
        insert(RoomsOrm)
        .values(
            hotel_id=hotel.id,
            title="Test Title",
            description="Test Description",
            price="10000",
            quantity="10",
        )
        .returning(RoomsOrm)
    ).scalar_one()
    db_session.commit()
    return res
