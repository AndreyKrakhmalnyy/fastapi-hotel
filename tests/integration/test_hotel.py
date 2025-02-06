from app.schemas.hotels import HotelIn
from app.utils.db_manager import DBManager
from app.database import async_session_maker


async def test_post_hotel():
    hotel_data = HotelIn(
        title="Test Hotel Title", location="Test Hotel Location"
    )
    async with DBManager(session_factory=async_session_maker) as db:
        await db.hotels.add_one(hotel_data)
        await db.commit()
