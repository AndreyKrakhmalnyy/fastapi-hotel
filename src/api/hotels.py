from fastapi import APIRouter, HTTPException, Query, Body
from models.hotels import HotelOrm
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelPutPost, HotelPatch
from src.database import async_session_maker
from sqlalchemy import insert


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "location": "Sochi", "title": "PULLMAN"},
    {"id": 2, "location": "Dubai", "title": "Rove Dubai Marina"},
    {"id": 3, "location": "Moscow", "title": "Azimut"},
    {"id": 4, "location": "Gelendzhik", "title": "Приморье"},
    {"id": 5, "location": "Paris", "title": "Hotel de Crillon"},
    {"id": 6, "location": "Rome", "title": "Hotel de Russie"},
    {"id": 7, "location": "London", "title": "The Ritz London"},
    {"id": 8, "location": "New York", "title": "The Peninsula New York"},
    {"id": 9, "location": "Tokyo", "title": "Imperial Hotel"},
    {"id": 10, "location": "Sydney", "title": "Four Seasons Hotel Sydney"},
]


@router.get(
    "",
    summary="Получение данных об отеле",
    description="Позволяет получить список всех отелей, либо конкретный по id.",
)
def get_hotel(
    pagination: PaginationDep,
    id: int | None = Query(None, description="Уникальный id отеля"),
    location: str | None = Query(None, description="Город"),
    title: str | None = Query(None, description="Название отеля"),
):
    all_hotels = []

    if pagination.per_page and pagination.page:
        return hotels[(pagination.per_page * pagination.page) - pagination.per_page:pagination.per_page * pagination.page]
    
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        elif location and hotel["location"] != location:
            continue
        elif title and hotel["title"] != title:
            continue
        all_hotels.append(hotel)
    return all_hotels


@router.post(
    "",
    summary="Добавление данных об отеле",
    description="Позволяет добавить данные по новому отелю.",
)
async def create_hotel(
    hotel_data: HotelPutPost = Body(
        openapi_examples={
            "1": {
                "summary": "Санкт-Петербург",
                "value": {"location": "Санкт-Петербург", "title": "Азимут"},
            }
        }
    )
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле",
    description="Принимает существующий id отеля и обновляет данные только при изменения значений для всех полей",
)
def put_hotel(hotel_id: int, hotel_data: HotelPutPost):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel.update({"location": hotel_data.location, "hotel_title": hotel_data.title})
            return {"status": "OK"}
    raise HTTPException(
        status_code=404, detail="The object with the entered 'hotel_id' is not found"
    )  # Возбудить исключение если введённый hotel_id не существует


@router.delete("/{hotel_id}", summary="Удаление данных об отеле")
def delete_hotel(hotel_id: int):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotels.remove(hotel)
            return {"status": "200 OK"}
    raise HTTPException(
        status_code=404, detail="The object with the entered 'hotel_id' is not found"
    )  # Возбудить исключение если введённый hotel_id не существует


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Принимает существующий id отеля и позволяет изменять данные только по нужным полям.",
)
def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.location is not None:
                hotel["location"] = hotel_data.location
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            return {"status": "OK"}
        raise HTTPException(
            status_code=404,
            detail="The object with the entered 'hotel_id' is not found",
        )  # Возбудить исключение если введённый hotel_id не существует
