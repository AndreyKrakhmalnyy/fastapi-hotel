from app.models.bookings import BookingsOrm
from app.models.facilities import FacilitiesOrm
from app.models.hotels import HotelsOrm
from app.models.rooms import RoomsOrm
from app.models.users import UsersOrm
from app.repositories.mappers.base import DataMapper
from app.schemas.bookings import BookingOut
from app.schemas.facilities import FacilityOut
from app.schemas.hotels import HotelOut
from app.schemas.rooms import RoomOut
from app.schemas.users import UserOut


class HotelsDataMapper(DataMapper):
    db_model = HotelsOrm
    api_model = HotelOut


class RoomsDataMapper(DataMapper):
    db_model = RoomsOrm
    api_model = RoomOut


class RoomsWithFacilitiesDataMapper(DataMapper):
    db_model = RoomsOrm
    api_model = RoomOut


class BookingsDataMapper(DataMapper):
    db_model = BookingsOrm
    api_model = BookingOut


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    api_model = FacilityOut


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    api_model = UserOut
