from sqlalchemy import func, select
from schemas.hotels import Hotel
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_alll(self, location, title, limit, offset):
        query = select(HotelsOrm)

        if location:
            query = query.filter(
                func.lower(HotelsOrm.location).contains(f"%{location.strip().lower()}%")
            )
        if title:
            query = query.filter(
                func.lower(HotelsOrm.title).contains(f"%{title.strip().lower()}%")
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [
            Hotel.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]