from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.facilities import FacilityOut
from app.schemas.tools import partial_model


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: Optional[List[int]] = []


class RoomIn(BaseModel):
    hotel_id: int
    title: str = Field(description="Название номера")
    description: str | None = Field(
        None, description="Описание номера"
    )
    price: int = Field(description="Цена за сутки")
    quantity: int = Field(description="Количество номеров отеля")


class RoomOut(RoomIn):
    id: int


class RoomWithFacilityOut(RoomOut):
    facilities: List[FacilityOut]


@partial_model
class RoomPatchRequest(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
    facilities_ids: List[int] = []


class RoomPatch(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int
