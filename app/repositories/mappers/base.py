from typing import Type, TypeVar
from pydantic import BaseModel
from app.database import Base

APIModel = TypeVar("APIModel", bound=BaseModel)
DBModel = TypeVar("DBModel", bound=Base)


class DataMapper:
    db_model = None
    api_model = None

    @classmethod
    def map_to_api_entity(cls, data) -> Type[APIModel]:
        return cls.api_model.model_validate(
            data, from_attributes=True
        )

    @classmethod
    def map_to_db_entity(cls, data) -> Type[DBModel]:
        return cls.db_model(**data.model_dump())
