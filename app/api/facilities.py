from fastapi import APIRouter, Body
from app.api.dependencies import DBDep
from app.schemas.facilities import (
    FacilityIn,
    RoomFacilityPartialUpdate,
)

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    "/all",
    summary="Получение данных о всех удобствах номера",
    description="Позволяет получить данные о удобствах в номере.",
)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.get(
    "/{facility_id}",
    summary="Получение данных об удобствах",
    description="Позволяет получить данные об удобствах в номере.",
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


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об удобствах",
    description="Позволяет частично обновить данные об удобствах в номере.",
)
async def patch_facilities(
    db: DBDep,
    hotel_id,
    facility_data: RoomFacilityPartialUpdate = Body(),
):
    facilities_data = await db.facilities.edit_partialy(
        facility_data, exclude_unset=True, id=hotel_id
    )
    await db.commit()
    return {"status": "OK", "data": facilities_data}
