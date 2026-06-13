from enum import StrEnum

from pydantic import BaseModel, Field


class FoodSource(StrEnum):
    TEXT = "text"
    PHOTO_DISH = "photo_dish"
    PHOTO_PRODUCT = "photo_product"


class FoodEventCreate(BaseModel):
    telegram_id: int
    description: str = Field(min_length=1)
    xe: float = Field(ge=0)
    bje: float = Field(ge=0)
    proteins: float | None = None
    fats: float | None = None
    carbs: float | None = None
    source: FoodSource
    request_id: str | None = None
    comment: str | None = None


class InsulinEventCreate(BaseModel):
    telegram_id: int
    dose: float = Field(gt=0)
    food_event_id: str | None = None
    injected_at: str | None = None
    comment: str | None = None


class EventCreated(BaseModel):
    id: str
    recorded_at: str
