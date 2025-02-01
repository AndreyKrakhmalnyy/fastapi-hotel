from sqlalchemy import select
from datetime import date
from app.schemas.bookings import BookingOut
from app.models.bookings import BookingsOrm
from app.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingOut

    async def get_today_bookings(self):
        query = select(BookingsOrm).filter(
            BookingsOrm.date_from == date.today()
        )
        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking)
            for booking in res.scalars().all()
        ]
