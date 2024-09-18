from fastapi import Body, FastAPI, HTTPException, Query
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "city": "Sochi", "name": "PULLMAN"},
    {"id": 2, "city": "Dubai", "name": "Rove Dubai Marina"},
    {"id": 3, "city": "Moscow", "name": "Azimut"},
    {"id": 4, "city": "Gelendzhik", "name": "Приморье"},
]


@app.get("/hotels", summary="Получение данных об отеле")
def get_hotel(
    id: int | None = Query(None, description="Уникальный id отеля"),
    city: str | None = Query(None, description="Город"),
    name: str | None = Query(None, description="Название отеля"),
):
    all_hotels = []

    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        elif city and hotel["city"] != city:
            continue
        elif name and hotel["name"] != name:
            continue
        all_hotels.append(hotel)
    return all_hotels


@app.post("/hotels", summary="Добавление данных об отеле")
def create_hotel(
    city: str = Body(embed=True, description="Город"),
    name: str = Body(embed=True, description="Название отеля"),
):
    global hotels

    if city != "string" and name != "string":
        hotels.append({"id": hotels[-1]["id"] + 1, "city": city, "name": name})
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}", summary="Удаление данных об отеле")
def delete_hotel(hotel_id: int):
    global hotels
    
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotels.remove(hotel)
            return {"status": "200 OK"}
    raise HTTPException(
        status_code=404, detail="The object with the entered 'hotel_id' is not found"
    ) # Возбудить исключение если введённый hotel_id не существует

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
