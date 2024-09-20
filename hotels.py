from fastapi import APIRouter, HTTPException, Query, Body
from schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "city": "Sochi", "name": "PULLMAN"},
    {"id": 2, "city": "Dubai", "name": "Rove Dubai Marina"},
    {"id": 3, "city": "Moscow", "name": "Azimut"},
    {"id": 4, "city": "Gelendzhik", "name": "Приморье"},
    {"id": 5, "city": "Paris", "name": "Hotel de Crillon"},
    {"id": 6, "city": "Rome", "name": "Hotel de Russie"},
    {"id": 7, "city": "London", "name": "The Ritz London"},
    {"id": 8, "city": "New York", "name": "The Peninsula New York"},
    {"id": 9, "city": "Tokyo", "name": "Imperial Hotel"},
    {"id": 10, "city": "Sydney", "name": "Four Seasons Hotel Sydney"},
]


@router.get(
    "",
    summary="Получение данных об отеле",
    description="Позволяет получить список всех отелей, либо конкретный по id.",
)
def get_hotel(
    id: int | None = Query(None, description="Уникальный id отеля"),
    city: str | None = Query(None, description="Город"),
    name: str | None = Query(None, description="Название отеля"),
    per_page: int = Query(None, description="Число отелей на странице"),
    page: int = Query(None, description="Номер страницы"),
):
    all_hotels = []

    if per_page and page:
        return hotels[(per_page * page) - per_page:per_page * page]
    if not page and per_page:
        return hotels[(per_page * 1) - per_page:per_page * 1]
    if not per_page and page:
        return hotels[(1 * page) - 1:1 * page]
    
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        elif city and hotel["city"] != city:
            continue
        elif name and hotel["name"] != name:
            continue
        all_hotels.append(hotel)
    return all_hotels


@router.post(
    "",
    summary="Добавление данных об отеле",
    description="Позволяет добавить данные по новому отелю.",
)
def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Санкт-Петербург",
                "value": {"city": "Санкт-Петербург", "name": "Азимут"},
            }
        }
    )
):
    global hotels

    if hotel_data.city != "string" and hotel_data.name != "string":
        hotels.append(
            {
                "id": hotels[-1]["id"] + 1,
                "city": hotel_data.city,
                "name": hotel_data.name,
            }
        )
    return {"status": "OK"}


@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле",
    description="Принимает существующий id отеля и обновляет данные только при изменения значений для всех полей",
)
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel.update({"city": hotel_data.city, "hotel_name": hotel_data.name})
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
            if hotel_data.city is not None:
                hotel["city"] = hotel_data.city
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {"status": "OK"}
        raise HTTPException(
            status_code=404,
            detail="The object with the entered 'hotel_id' is not found",
        )  # Возбудить исключение если введённый hotel_id не существует
