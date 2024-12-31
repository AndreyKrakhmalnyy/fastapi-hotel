from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: Optional[List[int]] = None


class RoomAdd(BaseModel):
    hotel_id: int
    title: str = Field(description="Название номера")
    description: str | None = Field(
        None, description="Описание номера"
    )
    price: int = Field(description="Цена за сутки")
    quantity: int = Field(description="Количество номеров отеля")


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
