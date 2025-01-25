from fastapi import APIRouter, Body
from app.schemas.bookings import BookingIn, BookingRequestAdd
from app.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/all")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_bookings_of_user(db: DBDep, user_id: UserIdDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "OK", "data": bookings}


@router.post("")
async def post_bookings(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingRequestAdd = Body(),
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    _booking_data = BookingIn(
        user_id=user_id, price=room_price, **booking_data.model_dump()
    )
    booking = await db.bookings.add_one(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
