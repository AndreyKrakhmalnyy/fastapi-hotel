from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class BookingRequestAdd(BaseModel):
    room_id: int
    date_from: date = Field(description="Дата начала бронирования")
    date_to: date = Field(description="Дата конца бронирования")


class BookingIn(BaseModel):
    user_id: int
    room_id: int
    date_from: date = Field(description="Дата начала бронирования")
    date_to: date = Field(description="Дата конца бронирования")
    price: int = Field(description="Стоимость номера за сутки")


class BookingOut(BookingIn):
    id: int

    model_config = ConfigDict(from_attributes=True)
