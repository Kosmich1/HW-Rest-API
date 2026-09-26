# app/schemas.py
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


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
    created_at: Optional[date] = None
    created_from: Optional[date] = None
    created_to: Optional[date] = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def check_ranges(self):
        if (self.price_min is not None and self.price_max is not None
                and self.price_min > self.price_max):
            raise ValueError("price_min не может быть больше price_max")
        if (self.created_from is not None and self.created_to is not None
                and self.created_from > self.created_to):
            raise ValueError("created_from не может быть позже created_to")
        return self


class SearchAdvertisementResponse(BaseModel):
    results: list[GetAdvertisementResponse]


class OKResponse(BaseModel):
    status: str = "ok"
