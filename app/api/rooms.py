from datetime import date
from fastapi import APIRouter, Body, Query
from app.schemas.facilities import RoomFacilityIn
from app.schemas.rooms import (
    RoomIn,
    RoomAddRequest,
    RoomPatch,
    RoomPatchRequest,
)
from app.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms/all",
    summary="Получение списка всех номеров",
)
async def get_rooms(
    db: DBDep,
    title: str | None = Query(None, description="Название номера"),
    price: int | None = Query(None, description="Цена за сутки"),
):
    return await db.rooms.get_rooms_filters(title=title, price=price)


@router.get(
    "/{hotel_id}/rooms",
    summary="Получение свободных номеров по дате заезда и выезда",
)
async def get_free_rooms_by_date(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-10-05"),
    date_to: date = Query(example="2024-10-10"),
):
    room = await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )
    return {"status": "OK", "data": room}


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение данных о номере конкретного отеля",
)
async def get_room_of_hotel(db: DBDep, hotel_id: int, room_id: int):
    room = await db.rooms.get_one_or_none_with_rels(
        id=room_id, hotel_id=hotel_id
    )
    return {"status": "OK", "data": room}


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавление данных о номере в отель",
)
async def post_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(),
):
    _room_data = RoomIn(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add_one(_room_data)

    rooms_ficilities_data = [
        RoomFacilityIn(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_batch(rooms_ficilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное обновление данных о номере конкретного отеля",
)
async def put_room(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest
):
    _room_data = RoomIn(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit_full(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(
        room_id, facilities_ids=room_data.facilities_ids
    )
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных об номере отеля",
)
async def patch_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit_partialy(
        _room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
    )
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление данных о номере по его id",
)
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete_by_id(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
