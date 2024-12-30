from pydantic import BaseModel, Field


class RoomAddRequest(BaseModel):
    title: str = Field(description="Название номера")
    description: str | None = Field(
        None, description="Описание номера"
    )
    price: int = Field(description="Цена за сутки")
    quantity: int = Field(description="Количество номеров отеля")


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
