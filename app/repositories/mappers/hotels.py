from app.models.hotels import HotelsOrm
from app.repositories.mappers.base import DataMapper
from app.schemas.hotels import HotelOut


class HotelsDataMapper(DataMapper):
    db_model = HotelsOrm
    api_model = HotelOut
