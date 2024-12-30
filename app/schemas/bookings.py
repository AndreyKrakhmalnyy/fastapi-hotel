from pydantic import BaseModel, Field
from datetime import date


class BookingRequestAdd(BaseModel):
    room_id: int
    date_from: date = Field(description="Дата начала бронирования")
    date_to: date = Field(description="Дата конца бронирования")


class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date = Field(description="Дата начала бронирования")
    date_to: date = Field(description="Дата конца бронирования")
    price: int = Field(description="Стоимость номера за сутки")


class Booking(BookingAdd):
    id: int
