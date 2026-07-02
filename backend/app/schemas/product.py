from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class StoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    logo_url: str | None = None


class ProductBase(BaseModel):
    title: str
    slug: str
    brand: str | None = None
    category: str | None = None
    image_url: str | None = None
    description: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class ProductPriceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    store_id: int
    current_price: Decimal
    availability: bool
    affiliate_url: HttpUrl | str
    updated_at: datetime
    store: StoreRead


class ProductSourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_name: str
    external_product_id: str
    product_url: str | None = None


class AffiliateLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    provider: str
    affiliate_url: str
    short_url: str | None = None
    tracking_id: str | None = None
    status: str
    click_count: int
    last_generated: datetime


class AvailabilityStatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    provider: str
    status: str
    quantity: int | None = None
    last_checked: datetime
    last_changed: datetime


class ProductAnalyticsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date
    views: int
    searches: int
    affiliate_clicks: int
    wishlist_adds: int
    compare_adds: int
    detail_page_visits: int
    score: int


class ProductSourceDetailRead(ProductSourceRead):
    affiliate_links: list[AffiliateLinkRead] = Field(default_factory=list)
    availability_statuses: list[AvailabilityStatusRead] = Field(default_factory=list)


class ProductListRead(ProductRead):
    prices: list[ProductPriceRead] = Field(default_factory=list)
    sources: list[ProductSourceRead] = Field(default_factory=list)


class ProductDetail(ProductRead):
    prices: list[ProductPriceRead] = Field(default_factory=list)
    sources: list[ProductSourceDetailRead] = Field(default_factory=list)
    analytics: list[ProductAnalyticsRead] = Field(default_factory=list)
    specifications: dict[str, str] = Field(default_factory=dict)
