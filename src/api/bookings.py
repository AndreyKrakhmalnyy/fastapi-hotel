from fastapi import APIRouter, Body
from schemas.bookings import BookingAdd, BookingRequestAdd
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("/{room_id}")
async def post_bookings(
    db: DBDep, 
    user_id: UserIdDep,
    room_id: int, 
    booking_data: BookingRequestAdd = Body()
):
    _booking_data = BookingAdd(room_id=room_id, user_id=user_id, **booking_data.model_dump())
    booking = await db.bookings.add_one(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
