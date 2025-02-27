from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from app.config import settings


engine = create_async_engine(settings.DB_URL)
# Пулл соединений, который не содержит соединений, а лишь открывает и закрывает сессию - для запуска celery_beat
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pool = async_sessionmaker(
    bind=engine_null_pool, expire_on_commit=False
)

session = async_session_maker()


class Base(DeclarativeBase):
    pass
