from pydantic import BaseModel, Field
from datetime import date

class BookingRequestAdd(BaseModel):
    date_from: date = Field(description='Дата начала бронирования')
    date_to: date = Field(description='Дата конца бронирования')

class BookingAdd(BaseModel):
    room_id: int
    date_from: date = Field(description='Дата начала бронирования')
    date_to: date = Field(description='Дата конца бронирования')    

class Booking(BookingAdd):
    id: int