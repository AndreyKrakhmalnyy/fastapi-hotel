from datetime import date
from app.repositories.utils import rooms_ids_for_booking
from app.schemas.rooms import Room, RoomWithFacility
from app.models.rooms import RoomsOrm
from app.repositories.base import BaseRepository
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_rooms_filters(self, title, price):
        query = select(RoomsOrm)

        if title:
            query = query.filter(
                func.lower(RoomsOrm.title).contains(
                    f"%{title.strip().lower()}%"
                )
            )
        if price:
            query = query.where(RoomsOrm.price == price)
        result = await self.session.execute(query)
        return [
            Room.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from, date_to, hotel_id
        )
        return await self.get_filtered(
            RoomsOrm.id.in_(rooms_ids_to_get)
        )

    async def get_one_or_none_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return RoomWithFacility.model_validate(model)
