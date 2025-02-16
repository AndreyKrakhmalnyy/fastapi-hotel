from typing import Type, TypeVar
from pydantic import BaseModel
from app.database import Base

APIModelType = TypeVar("APIModelType", bound=BaseModel)
DBModelType = TypeVar("DBModelType", bound=Base)


class DataMapper:
    api_model: Type[APIModelType] = None
    db_model: Type[DBModelType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.api_model.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_db_entity(cls, data) -> DBModelType:
        return cls.db_model(**data.model_dump())
