from pydantic import BaseModel, Field


class HotelPutPost(BaseModel):
    city: str = Field(None, description="Город")
    name: str = Field(None, description="Название отеля")
    
class HotelPatch(BaseModel):
    city: str | None = Field(None, description="Город")
    name: str | None = Field(None, description="Название отеля")