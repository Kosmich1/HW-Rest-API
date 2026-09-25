# app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import config

# Создаём асинхронный движок
engine = create_async_engine(config.DATABASE_URL)

# Фабрика сессий. expire_on_commit=False - чтобы можно было работать с объектами после коммита.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для наших моделей
Base = declarative_base()
