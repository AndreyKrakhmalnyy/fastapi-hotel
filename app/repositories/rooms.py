from datetime import date
from app.repositories.mappers.base import DataMapper
from app.repositories.mappers.mappers import (
    RoomsDataMapper,
    RoomsWithFacilitiesDataMapper,
)
from app.repositories.utils import rooms_ids_for_booking
from app.models.rooms import RoomsOrm
from app.repositories.base import BaseRepository
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper: DataMapper = RoomsDataMapper

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
            self.mapper.map_to_domain_entity(model)
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
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomsWithFacilitiesDataMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

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
        return RoomsWithFacilitiesDataMapper.map_to_domain_entity(
            model
        )
