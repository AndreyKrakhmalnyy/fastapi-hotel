import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from app.api.hotels import router as router_hotels
from app.api.auth import router as router_auth
from app.api.rooms import router as router_rooms
from app.api.bookings import router as router_bookings
from app.api.facilities import router as facility_hotels

app = FastAPI()
app.include_router(router_hotels)
app.include_router(router_auth)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(facility_hotels)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
