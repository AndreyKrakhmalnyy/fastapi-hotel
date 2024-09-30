from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session) -> None:
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]

    async def get_by_id(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return (
            None
            if model is None
            else self.schema.model_validate(model, from_attributes=True)
        )

    async def add_one(self, data: BaseModel):
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(query)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit_full(self, data: BaseModel, **filter_by):
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(query)
        model = result.scalar()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit_partialy(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ):
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(query)
        model = result.scalar()
        return self.schema.model_validate(model, from_attributes=True)

    async def delete_by_id(self, **filter_by):
        query = delete(self.model).filter_by(**filter_by)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(query)