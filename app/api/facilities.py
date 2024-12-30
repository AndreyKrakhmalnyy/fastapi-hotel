from fastapi import APIRouter, Body
from app.api.dependencies import DBDep
from app.schemas.facilities import FacilityIn

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    "",
    summary="Получение данных об удобствах",
    description="Позволяет получить данные об удобствах в номере.",
)
async def get_facility(db: DBDep, facility_id: int):
    facility = await db.facilities.get_one_or_none(id=facility_id)
    await db.commit()
    return {"status": "OK", "data": facility}


@router.post(
    "",
    summary="Добавление данных об удобствах",
    description="Позволяет добавить данные об удобствах в номере.",
)
async def post_facility(
    db: DBDep, facility_data: FacilityIn = Body()
):
    facility = await db.facilities.add_one(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
