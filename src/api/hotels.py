from repositories.hotels import HotelsRepository
from fastapi import APIRouter, Query, Body
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
        return await HotelsRepository(session).get_full(
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
async def post_hotel(
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
    description="Принимает существующий id отеля и обновляет данные только при изменения значений для всех полей.",
)
async def put_hotel(hotel_id: int, hotel_data: HotelsPutPost):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit_full(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK", "data": hotel}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Принимает существующий id отеля как обязательный параметр и позволяет изменять данные только по нужным полям.",
)
async def patch_hotel(hotel_id: int, hotel_data: HotelsPatch):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit_partialy(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
        return {"status": "OK", "data": hotel}

@router.delete(
    "/{hotel_id}",
    summary="Удаление данных об отеле по его id",
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete_by_id(id=hotel_id)
        await session.commit()
    return {"status": "OK"}