from pydantic import BaseModel, ConfigDict


class FacilityIn(BaseModel):
    title: str


class FacilityOut(FacilityIn):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomFacilityIn(BaseModel):
    room_id: int
    facility_id: int


class RoomFacilityOut(RoomFacilityIn):
    id: int
