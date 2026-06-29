from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, HttpUrl


class PriceObservation(BaseModel):
    title: str
    brand: str | None = None
    category: str | None = "Gaming Laptops"
    image_url: str | None = None
    description: str | None = None
    price: Decimal
    availability: bool
    affiliate_url: HttpUrl | str
    store: str
    store_logo_url: str | None = None


class PriceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    store_id: int
    current_price: Decimal
    availability: bool
    affiliate_url: HttpUrl | str
    updated_at: datetime


class PriceHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    store_id: int
    price: Decimal
    created_at: datetime
