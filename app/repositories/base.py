from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update

from app.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session) -> None:
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model).filter(*filter).filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_api_entity(model)
            for model in result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        return (
            None
            if model is None
            else self.mapper.map_to_api_entity(
                model, from_attributes=True
            )
        )

    async def add_one(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_api_entity(model)

    async def add_batch(self, data: list[BaseModel]):
        query = insert(self.model).values(
            [item.model_dump() for item in data]
        )
        await self.session.execute(query)

    async def edit_full(self, data: BaseModel, **filter_by):
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(query)
        model = result.scalar()
        return self.mapper.map_to_api_entity(
            model, from_attributes=True
        )

    async def edit_partialy(
        self,
        data: BaseModel,
        exclude_unset: bool = False,
        **filter_by,
    ):
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(query)
        model = result.scalar()
        print(query.compile(compile_kwargs={"literal_binds": True}))
        return self.mapper.map_to_api_entity(
            model, from_attributes=True
        )

    async def delete_by_id(self, **filter_by):
        query = delete(self.model).filter_by(**filter_by)
        await self.session.execute(query)
