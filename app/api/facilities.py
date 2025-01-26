import json
from fastapi import APIRouter, Body
from app.api.dependencies import DBDep
from app.schemas.facilities import (
    FacilityIn,
)
from app.redis_client import redis_manager

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    "/all",
    summary="Получение данных о всех удобствах номера",
    description="Позволяет получить данные о удобствах в номере.",
)
async def get_facilities(db: DBDep):
    cached_facilities = await redis_manager.get("facilities")
    if not cached_facilities:
        print("DB")
        db_facilities = await db.facilities.get_all()
        schemas_facilities = [f.model_dump() for f in db_facilities]
        await redis_manager.set(
            "facilities", json.dumps(schemas_facilities), 5
        )

        return db_facilities
    return json.loads(cached_facilities)


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
