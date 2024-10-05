from schemas.rooms import Room
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