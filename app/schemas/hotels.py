from pydantic import BaseModel, ConfigDict, Field


class HotelAdd(BaseModel):
    location: str = Field(None, description="Город")
    title: str = Field(None, description="Название отеля")


class Hotel(HotelAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class HotelPatch(BaseModel):
    location: str | None = Field(None, description="Город")
    title: str | None = Field(None, description="Название отеля")
