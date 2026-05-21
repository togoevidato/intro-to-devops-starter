from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class FruitEntity(Base):
    __tablename__ = "fruits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    in_season: Mapped[bool] = mapped_column(Boolean, nullable=False)


class FruitCreate(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    in_season: bool


class FruitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    price: float | None = Field(default=None, gt=0)
    in_season: bool | None = None


class Fruit(BaseModel):
    id: int
    name: str
    price: float
    in_season: bool

    model_config = {
        "from_attributes": True
    }