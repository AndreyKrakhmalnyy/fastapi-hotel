from fastapi import APIRouter, Body
from app.api.dependencies import DBDep
from app.schemas.facilities import (
    FacilityIn,
)
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    "/all",
    summary="Получение данных о всех удобствах номера",
    description="Позволяет получить данные о удобствах в номере.",
)
@cache(expire=5)
async def get_facilities(db: DBDep):
    print("DB")
    return await db.facilities.get_all()


@router.get(
    "/{facility_id}",
    summary="Получение данных об удобствах по id",
    description="Позволяет получить данные об удобствах в номере по id.",
)
async def get_facility(db: DBDep, facility_id: int):
    facility = await db.facilities.get_one_or_none(id=facility_id)
    return {"status": "OK", "data": facility}


@router.post(
    "",
    summary="Добавление данных об удобствах",
    description="Позволяет добавить данные об удобствах в номере.",
)
async def post_facility(
    db: DBDep, facility_data: FacilityIn = Body()
):
    facilities_data = await db.facilities.add_one(facility_data)
    await db.commit()
    return {"status": "OK", "data": facilities_data}
