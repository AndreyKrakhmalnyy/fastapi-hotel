from app.models.facilities import FacilitiesOrm
from app.repositories.base import BaseRepository
from app.schemas.facilities import FacilityOut


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = FacilityOut
