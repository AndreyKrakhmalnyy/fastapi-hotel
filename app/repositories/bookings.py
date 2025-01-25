from app.schemas.bookings import BookingOut
from app.models.bookings import BookingsOrm
from app.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingOut
