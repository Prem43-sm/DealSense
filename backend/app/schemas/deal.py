from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.schemas.product import ProductRead


class DealRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    deal_score: int
    discount_percent: Decimal
    created_at: datetime
    product: ProductRead
