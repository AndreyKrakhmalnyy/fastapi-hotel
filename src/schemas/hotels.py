from pydantic import BaseModel, Field


class HotelPutPost(BaseModel):
    location: str = Field(None, description="Город")
    title: str = Field(None, description="Название отеля")
    
class HotelPatch(BaseModel):
    location: str | None = Field(None, description="Город")
    title: str | None = Field(None, description="Название отеля")