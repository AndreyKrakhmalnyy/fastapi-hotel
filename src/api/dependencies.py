from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel
from typing import Annotated
from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    per_page: Annotated[
        int | None, Query(None, description="Число отелей на странице", ge=1)
    ]
    page: Annotated[int | None, Query(1, description="Номер страницы", ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(
            status_code=401, detail="Вы не авторизованы, предоставьте токен доступа"
        )
    return token


def get_current_user_by_id(token: str = Depends(get_token)):
    user_data = AuthService().decode_token(token)
    user_id = user_data.get("user_id", None)
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_by_id)]
UserTokenDep = Annotated[int, Depends(get_token)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
