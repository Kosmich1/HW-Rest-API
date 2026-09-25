# app/app.py

from typing import Annotated

from fastapi import Depends, FastAPI, Query
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from dependencies import get_db_session
from lifespan import lifespan
from services import (add_item, delete_item, get_item, search_advertisements,
                      update_item)

app = FastAPI(
    title="Advertisements",
    description="Сервис объявлений купли/продажи",
    version="0.0.1",
    lifespan=lifespan
)

# Создаём тип для зависимости сессии
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


@app.post(
    "/advertisement",
    response_model=schemas.CreateAdvertisementResponse,
    status_code=201,
    summary="Создать объявление",
)
async def create_advertisement(
        advertisement_data: schemas.CreateAdvertisementRequest,
        session: SessionDep
):
    advertisement = await add_item(session, models.Advertisement, advertisement_data)
    return schemas.CreateAdvertisementResponse(id=advertisement.id)


@app.get(
    "/advertisement",
    response_model=schemas.SearchAdvertisementResponse,
    summary="Поиск объявлений по полям",
)
async def search_advertisement(
        params: Annotated[schemas.SearchAdvertisementParams, Query()],
        session: SessionDep
):
    advertisements = await search_advertisements(session, params)
    return schemas.SearchAdvertisementResponse(
        results=[advertisement.to_dict() for advertisement in advertisements]
    )


@app.get(
    "/advertisement/{advertisement_id}",
    response_model=schemas.GetAdvertisementResponse,
    summary="Получить объявление по ID",
)
async def get_advertisement(
        advertisement_id: int,
        session: SessionDep
):
    advertisement = await get_item(session, models.Advertisement, advertisement_id)
    return schemas.GetAdvertisementResponse(**advertisement.to_dict())


@app.patch(
    "/advertisement/{advertisement_id}",
    response_model=schemas.UpdateAdvertisementResponse,
    summary="Обновить объявление",
)
async def update_advertisement(
        advertisement_id: int,
        update_data: schemas.UpdateAdvertisementRequest,
        session: SessionDep
):
    advertisement = await update_item(
        session, models.Advertisement, advertisement_id, update_data
    )
    return schemas.UpdateAdvertisementResponse(**advertisement.to_dict())


@app.delete(
    "/advertisement/{advertisement_id}",
    response_model=schemas.OKResponse,
    summary="Удалить объявление",
)
async def delete_advertisement(
        advertisement_id: int,
        session: SessionDep
):
    await delete_item(session, models.Advertisement, advertisement_id)
    return schemas.OKResponse()
