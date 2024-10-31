from datetime import date
from src.models.bookings import BookingsOrm
from src.schemas.rooms import Room
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from sqlalchemy import func, select


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_rooms_filters(self, title, price):
        query = select(RoomsOrm)

        if title:
            query = query.filter(
                func.lower(RoomsOrm.title).contains(f"%{title.strip().lower()}%")
            )
        if price:
            query = query.where(RoomsOrm.price == price)
        result = await self.session.execute(query)
        return [
            Room.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):

        cross_booked = (
            select(BookingsOrm.room_id, func.count("*").label(name="rooms_cnt"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_from,
                BookingsOrm.date_to >= date_to,
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="cross_booked")
        )

        free_rooms = (
            select(
                RoomsOrm.id.label(name="room_id"),
                (
                    RoomsOrm.quantity - func.coalesce(cross_booked.c.rooms_booked_cnt)
                ).label(name="free_rooms_cnt"),
            )
            .select_from(RoomsOrm)
            .join(cross_booked, cross_booked.c.room_id == RoomsOrm.id)
            .cte(name="free_rooms")
        )

        query = (
            select(free_rooms)
            .select_from(free_rooms)
            .filter(free_rooms.c.free_rooms_cnt > 0)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
