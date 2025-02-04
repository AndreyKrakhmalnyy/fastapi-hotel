import pytest
from app.config import settings
from app.database import Base, engine_null_pool
from app.models import *  # flake8: ignore


@pytest.fixture(autouse=True)
async def async_main():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all())
