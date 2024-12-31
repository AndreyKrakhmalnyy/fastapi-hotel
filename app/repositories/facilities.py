from app.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from app.repositories.base import BaseRepository
from app.schemas.facilities import FacilityOut, RoomFacilityOut


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = FacilityOut


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacilityOut
