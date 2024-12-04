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

        cross_booked_cte = (
            select(BookingsOrm.room_id, func.count("*").label(name="rooms_count"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_from,
                BookingsOrm.date_to >= date_to,
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="cross_booked_cte")
        )

        free_rooms_join = (
            select(
                RoomsOrm.id.label(name="room_id"),
                (
                    RoomsOrm.quantity - func.coalesce(cross_booked_cte.c.rooms_count, 0)
                ).label(name="free_rooms_count"),
            )
            .select_from(RoomsOrm)
            .join(cross_booked_cte, cross_booked_cte.c.room_id == RoomsOrm.id)
            .cte(name="free_rooms_join")
        )

        room_ids_for_hotel = select(RoomsOrm.id).select_from(RoomsOrm).filter_by(hotel_id=hotel_id).subquery("rooms_of_hotel")

        query = (
            select(free_rooms_join)
            .select_from(free_rooms_join)
            .filter(free_rooms_join.c.free_rooms_count > 0,
                    #free_rooms.c.room_id.in_(room_ids_for_hotel)
            )
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
