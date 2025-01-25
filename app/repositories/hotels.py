from datetime import date
from sqlalchemy import func, select
from app.models.rooms import RoomsOrm
from app.repositories.mappers.base import DataMapper
from app.repositories.mappers.hotels import HotelsDataMapper
from app.repositories.utils import rooms_ids_for_booking
from app.schemas.hotels import HotelOut
from app.models.hotels import HotelsOrm
from app.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper: DataMapper = HotelsDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location,
        title,
        limit,
        offset,
    ) -> list[HotelOut]:
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from, date_to=date_to
        )
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(
            HotelsOrm.id.in_(hotels_ids_to_get)
        )
        if location:
            query = query.filter(
                func.lower(HotelsOrm.location).contains(
                    location.strip().lower()
                )
            )
        if title:
            query = query.filter(
                func.lower(HotelsOrm.title).contains(
                    title.strip().lower()
                )
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [
            self.mapper.api_model(hotel, from_attributes=True)
            for hotel in result.scalars().all()
        ]
