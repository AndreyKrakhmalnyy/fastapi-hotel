from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
import pytest
from app.database import Base, engine_null_pool
from app.models import *  # flake8: ignore
from app.main import app


# @pytest.fixture(scope="session", autouse=True)
# def check_test_mode():
#     assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="module")
async def api_client() -> AsyncGenerator:
    """Фикстура асинхронного клиента FastAPI"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as fast_client:
        yield fast_client
