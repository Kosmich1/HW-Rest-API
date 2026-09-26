# Сервис объявлений купли/продажи на FastAPI

Домашнее задание к лекции «Создание REST API на FastApi», часть 1 ([условие](./TASK.md)).

## Стек

FastAPI, SQLAlchemy 2 (async) + asyncpg, PostgreSQL, Docker.

## Объявление

| Поле | Тип | Описание |
|---|---|---|
| `id` | int | идентификатор |
| `title` | str | заголовок (обязательный) |
| `description` | str | описание |
| `price` | float | цена, ≥ 0 (обязательная) |
| `author` | str | автор (обязательный) |
| `created_at` | str | дата создания, проставляется автоматически |

## Методы

| Метод | URL | Описание |
|---|---|---|
| POST | `/advertisement` | создание |
| PATCH | `/advertisement/{advertisement_id}` | обновление (только переданные поля) |
| DELETE | `/advertisement/{advertisement_id}` | удаление |
| GET | `/advertisement/{advertisement_id}` | получение по id |
| GET | `/advertisement?{query_string}` | поиск по полям |

Параметры поиска (все необязательные, комбинируются между собой):

- `title`, `description`, `author` — поиск по вхождению подстроки без учёта регистра;
- `price_min`, `price_max` — диапазон цены;
- `created_at` — дата создания в формате `ГГГГ-ММ-ДД`: объявления, созданные в этот день (UTC);
- `created_from`, `created_to` — диапазон дат создания `ГГГГ-ММ-ДД`, обе границы включительно;
- `limit` (по умолчанию 20, максимум 100), `offset` — пагинация.

Примеры:

- `GET /advertisement?title=шкаф&author=иван&price_max=10000`
- `GET /advertisement?created_at=2026-09-26`
- `GET /advertisement?created_from=2026-09-01&created_to=2026-09-30`

Интерактивная документация Swagger: http://127.0.0.1:8080/docs

## Запуск в Docker

```bash
cp .env.example .env   # указать пароль для БД
docker compose up -d --build
```

API будет доступно на http://127.0.0.1:8080. Остановка: `docker compose down`.

## Запуск без Docker

```bash
pip install -r requirements.txt
cp .env.example .env   # указать данные локального PostgreSQL
createdb -U postgres netology_fastapi_ads
cd app
uvicorn app:app --port 8080
```
