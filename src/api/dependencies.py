from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated


class PaginationParams(BaseModel):
    per_page: Annotated[
        int | None, Query(None, description="Число отелей на странице", ge=1)
    ]
    page: Annotated[int | None, Query(1, description="Номер страницы", ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]
