import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.redis_client import redis_manager

from app.api.facilities import router as facility_router
from app.api.bookings import router as booking_router
from app.api.rooms import router as room_router
from app.api.auth import router as auth_router
from app.api.hotels import router as hotel_router
from app.api.images import router as image_router

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

app.include_router(hotel_router)
app.include_router(auth_router)
app.include_router(room_router)
app.include_router(booking_router)
app.include_router(facility_router)
app.include_router(image_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
