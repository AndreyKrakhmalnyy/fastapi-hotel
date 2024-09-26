from pydantic import BaseModel, Field


class HotelsPutPost(BaseModel):
    location: str = Field(None, description="Город")
    title: str = Field(None, description="Название отеля")
    
class HotelsPatch(BaseModel):
    location: str | None = Field(None, description="Город")
    title: str | None = Field(None, description="Название отеля")