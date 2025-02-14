from sqlalchemy import select
from datetime import date
from app.repositories.mappers.base import APIModelType
from app.repositories.utils import rooms_ids_for_booking
from app.schemas.bookings import BookingIn, BookingOut
from app.models.bookings import BookingsOrm
from app.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingOut

    async def get_today_bookings(self) -> list[APIModelType]:
        query = select(BookingsOrm).filter(
            BookingsOrm.date_from == date.today()
        )
        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking)
            for booking in res.scalars().all()
        ]

    async def add_booking(
        self, data: BookingIn, hotel_id: int
    ) -> APIModelType:
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        rooms_ids_to_book_res = await self.session.execute(
            rooms_ids_to_get
        )
        rooms_ids_to_book: list[int] = (
            rooms_ids_to_book_res.scalars().all()
        )
        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add_one(data)
            return new_booking
        else:
            raise Exception
