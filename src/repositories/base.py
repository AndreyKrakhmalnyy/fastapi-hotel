from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update


class BaseRepository:
    model = None

    def __init__(self, session) -> None:
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add_one(self, data: BaseModel):
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(query)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        return result.scalar()

    async def edit_partialy(self, data: BaseModel, **filter_by):
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def delete_by_id(self, **filter_by):
        query = delete(self.model).filter_by(**filter_by)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(query)
