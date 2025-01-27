from contextlib import asynccontextmanager
from app.api.facilities import router as facility_hotels
from app.api.bookings import router as router_bookings
from app.api.rooms import router as router_rooms
from app.api.auth import router as router_auth
from app.api.hotels import router as router_hotels
from app.redis_client import redis_manager
import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Управляет жизненным циклом приложения.

    Args:
        _ (FastAPI): Экземпляр FastAPI
    """
    await redis_manager.connect()
    FastAPICache.init(
        RedisBackend(redis_manager.redis), prefix="fastapi-cache"
    )
    yield
    await redis_manager.close()


app = FastAPI(root_path="/api", lifespan=lifespan)

app.include_router(router_hotels)
app.include_router(router_auth)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(facility_hotels)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
