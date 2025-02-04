"""Импорт всех модулей с моделями"""

from app.models.bookings import BookingsOrm
from app.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from app.models.hotels import HotelsOrm
from app.models.rooms import RoomsOrm
from app.models.users import UsersOrm


__all__ = [
    "BookingsOrm",
    "FacilitiesOrm",
    "RoomsFacilitiesOrm",
    "HotelsOrm",
    "RoomsOrm",
    "UsersOrm",
]
