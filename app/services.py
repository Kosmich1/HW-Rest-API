# app/services.py
from datetime import date, datetime, time, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def add_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_data: schemas.CreateAdvertisementRequest
) -> models.Advertisement:
    """
    Универсальная функция для добавления записи в БД.
    """
    new_item = orm_model(**item_data.model_dump())
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item


async def get_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_id: int
) -> models.Advertisement:
    """
    Получает запись по ID или выбрасывает 404.
    """
    item = await session.get(orm_model, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{orm_model.__name__} with id {item_id} not found"
        )
    return item


async def update_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_id: int,
        update_data: schemas.UpdateAdvertisementRequest
) -> models.Advertisement:
    """
    Обновляет только переданные поля записи.
    """
    item = await get_item(session, orm_model, item_id)

    # Берём только переданные поля; null для обязательных полей не допускаем
    update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in update_dict.items():
        setattr(item, key, value)

    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_id: int
) -> None:
    """
    Удаляет запись.
    """
    item = await get_item(session, orm_model, item_id)
    await session.delete(item)
    await session.commit()


def _day_start(day: date) -> datetime:
    """Начало суток (00:00 UTC) для указанной даты."""
    return datetime.combine(day, time.min, tzinfo=timezone.utc)


async def search_advertisements(
        session: AsyncSession,
        params: schemas.SearchAdvertisementParams
) -> list[models.Advertisement]:
    """
    Поиск объявлений: текстовые поля ищутся по вхождению без учёта регистра,
    цена — по диапазону, дата создания — за конкретный день или по диапазону дат.
    """
    Advertisement = models.Advertisement
    stmt = select(Advertisement)

    if params.title:
        stmt = stmt.where(Advertisement.title.ilike(f"%{params.title}%"))
    if params.description:
        stmt = stmt.where(Advertisement.description.ilike(f"%{params.description}%"))
    if params.author:
        stmt = stmt.where(Advertisement.author.ilike(f"%{params.author}%"))
    if params.price_min is not None:
        stmt = stmt.where(Advertisement.price >= params.price_min)
    if params.price_max is not None:
        stmt = stmt.where(Advertisement.price <= params.price_max)
    if params.created_at is not None:
        stmt = stmt.where(
            Advertisement.created_at >= _day_start(params.created_at),
            Advertisement.created_at < _day_start(params.created_at + timedelta(days=1)),
        )
    if params.created_from is not None:
        stmt = stmt.where(Advertisement.created_at >= _day_start(params.created_from))
    if params.created_to is not None:
        stmt = stmt.where(
            Advertisement.created_at < _day_start(params.created_to + timedelta(days=1))
        )

    stmt = stmt.order_by(Advertisement.created_at.desc(), Advertisement.id.desc())
    stmt = stmt.limit(params.limit).offset(params.offset)
    result = await session.scalars(stmt)
    return list(result)
