from repositories.hotels import HotelsRepository
from fastapi import APIRouter, HTTPException, Query, Body
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelsPutPost, HotelsPatch
from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение данных об отеле",
    description="Позволяет получить список всех отелей, либо конкретный по id.",
)
async def get_hotel(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Город"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@router.post(
    "",
    summary="Добавление данных об отеле",
    description="Позволяет добавить данные по новому отелю.",
)
async def create_hotel(
    hotel_data: HotelsPutPost = Body(
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
    async with async_session_maker() as session: 
        hotel = await HotelsRepository(session).add_one(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле",
    description="Принимает существующий id отеля и обновляет данные только при изменения значений для всех полей",
)
def put_hotel(hotel_id: int, hotel_data: HotelsPutPost):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel.update(
                {"location": hotel_data.location, "hotel_title": hotel_data.title}
            )
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
def patch_hotel(hotel_id: int, hotel_data: HotelsPatch):
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
