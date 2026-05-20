from pydantic import BaseModel, Field
from typing import Optional


class FruitCreate(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    in_season: bool


class FruitUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    price: Optional[float] = Field(default=None, gt=0)
    in_season: Optional[bool] = None


class Fruit(BaseModel):
    id: int
    name: str
    price: float
    in_season: bool