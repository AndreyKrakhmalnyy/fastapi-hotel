from datetime import date
from fastapi import APIRouter, Query, Body
from app.api.dependencies import DBDep, PaginationDep
from app.schemas.hotels import HotelAdd, HotelPatch
from app.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )

@router.get("/{hotel_id}", summary="Получение данных о конкретном отеле по его id")
async def get_hotel(db: DBDep, hotel_id: int):
        hotel = await db.hotels.get_one_or_none(id=hotel_id)
        return {"status": "OK", "data": hotel}


@router.post(
    "",
    summary="Добавление данных об отеле",
    description="Позволяет добавить данные по новому отелю.",
)
async def post_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Санкт-Петербург",
                "value": {"location": "Санкт-Петербург", "title": "Azimut Resort"},
            },
            "2": {
                "summary": "Геленджик",
                "value": {"location": "Геленджик", "title": "Elean Family"},
            },
            "3": {
                "summary": "Дубай",
                "value": {"location": "Дубай", "title": "Dubai Family Bearitz"},
            },
        }
    )
):
        hotel = await db.hotels.add_one(hotel_data)
        await db.commit()
        return {"status": "OK", "data": hotel}

@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле",
    description="Принимает существующий id отеля и обновляет данные только при изменения значений для всех полей.",
)
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
        hotel = await db.hotels.edit_full(hotel_data, id=hotel_id)
        await db.commit()
        return {"status": "OK", "data": hotel}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Принимает существующий id отеля как обязательный параметр и позволяет изменять данные только по нужным полям.",
)
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
        hotel = await db.hotels.edit_partialy(
            hotel_data, exclude_unset=True, id=hotel_id
        )
        await db.commit()
        return {"status": "OK", "data": hotel}
    
@router.delete(
    "/{hotel_id}",
    summary="Удаление данных об отеле по его id",
)
async def delete_hotel(db: DBDep, hotel_id: int):
        await db.hotels.delete_by_id(id=hotel_id)
        await db.commit()
        return {"status": "OK"}