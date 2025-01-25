from pydantic import BaseModel, Field


class HotelIn(BaseModel):
    location: str = Field(None, description="Город")
    title: str = Field(None, description="Название отеля")


class HotelOut(HotelIn):
    id: int


class HotelPatch(BaseModel):
    location: str | None = Field(None, description="Город")
    title: str | None = Field(None, description="Название отеля")
