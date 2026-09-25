# app/config.py
import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()  # Загружаем переменные из файла .env


class Config:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "netology_fastapi_ads")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    DATABASE_URL = URL.create(
        "postgresql+asyncpg",
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=int(POSTGRES_PORT),
        database=POSTGRES_DB,
    )


config = Config()
