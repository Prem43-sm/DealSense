from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    provider: str
    title: str
    brand: str | None = None
    category: str | None = None
    description: str | None = None
    image_url: str | None = None
    external_id: str
    product_url: str | None = None
    canonical_url: str | None = None


class PriceData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    provider: str
    external_id: str
    price: Decimal
    currency: str = "INR"


class AvailabilityData(BaseModel):
    provider: str
    external_id: str
    available: bool
    status: str = "unknown"


class AffiliateLinkData(BaseModel):
    provider: str
    external_id: str | None = None
    url: str
    sponsored: bool = True


class ConnectorHealth(BaseModel):
    provider: str
    status: str
    message: str | None = None

