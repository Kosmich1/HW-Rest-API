# app/schemas.py
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BaseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class CreateAdvertisementRequest(BaseRequest):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    price: float = Field(ge=0)
    author: str = Field(min_length=1, max_length=100)


class CreateAdvertisementResponse(BaseModel):
    id: int


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    created_at: Optional[str] = None


class UpdateAdvertisementRequest(BaseRequest):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    author: Optional[str] = Field(default=None, min_length=1, max_length=100)


class UpdateAdvertisementResponse(GetAdvertisementResponse):
    pass


class SearchAdvertisementParams(BaseRequest):
    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    price_min: Optional[float] = Field(default=None, ge=0)
    price_max: Optional[float] = Field(default=None, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class SearchAdvertisementResponse(BaseModel):
    results: list[GetAdvertisementResponse]


class OKResponse(BaseModel):
    status: str = "ok"
