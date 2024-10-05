from fastapi import APIRouter, Body, Query
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.database import async_session_maker
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms/all",
    summary="Получение списка всех номеров",
    description="Позволяет также фильтроваться по названию номера и цене за сутки.",
)
async def get_all_rooms(
    db: DBDep,
    title: str | None = Query(None, description="Название номера"),
    price: int | None = Query(None, description="Цена за сутки"),
):
        return await db.rooms.get_rooms_filters(title=title, price=price)
    
@router.get(
    "/{hotel_id}/rooms", 
    summary="Получение данных о всех номерах конкретного отеля"
)
async def get_rooms_of_hotel(db: DBDep, hotel_id: int):
        room = await db.rooms.get_filtered(hotel_id=hotel_id)
        return {"status": "OK", "data": room}

@router.get(
    "/{hotel_id}/rooms/{room_id}", summary="Получение данных о номере конкретного отеля"
)
async def get_room_of_hotel(db: DBDep, hotel_id: int, room_id: int):
        room = await db.rooms.get_one_or_none(
            id=room_id, hotel_id=hotel_id
        )
        return {"status": "OK", "data": room}

@router.post(
    "/{hotel_id}/rooms",
    summary="Добавление данных о номере в отель",
    description="Позволяет добавить данные по новому номеру в конретный отель.",
)
async def post_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "Санкт-Петербург": {
                "summary": "Azimut Resort",
                "value": {
                    "title": "Одноместный Luxury",
                    "description": "Люкс-номер для одного человека с одним спальным местом.",
                    "price": 10000,
                    "quantity": 15,
                },
            },
            "Геленджик": {
                "summary": "Elean Family",
                "value": {
                    "title": "Двухместный Deluxe",
                    "description": "Супер люкс-номер для двух человек с двумя спальными местами с джакузи.",
                    "price": 15000,
                    "quantity": 10,
                },
            },
            "Дубай": {
                "summary": "Dubai Family Bearitz",
                "value": {
                    "title": "Трёхкомнатный президентский",
                    "description": "Президентский люкс-номер для трёх человек с тремя спальными местами.",
                    "price": 50000,
                    "quantity": 5,
                },
            },
        }
    ),
):
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())  
        room = await db.rooms.add_one(_room_data)
        await db.commit()
        return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное обновление данных о номере конкретного отеля",
    description="Принимает существующий id отеля и номера как обязательные параметры и обновляет данные только при изменения значений для всех полей.",
)
async def put_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await db.rooms.edit_full(
            _room_data, hotel_id=hotel_id, id=room_id
        )
        await db.commit()
        return {"status": "OK", "data": room}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных об номере отеля",
    description="Принимает id отеля и номера как обязательные параметры и позволяет изменять данные только по нужным полям.",
)
async def patch_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
        _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
        room = await db.rooms.edit_partialy(
            _room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id
        )
        await db.commit()
        return {"status": "OK", "data": room}

@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление данных о номере по его id",
)
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
        await db.rooms.delete_by_id(id=room_id, hotel_id=hotel_id)
        await db.commit()
        return {"status": "OK"}
