from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from pydantic import BaseModel

from app.automation.agents.price_monitor.sources import SourcePrice


class NormalizedPrice(BaseModel):
    product_id: int
    store: str
    price: Decimal
    currency: str


def normalize_price(source_price: SourcePrice) -> NormalizedPrice | None:
    try:
        price = Decimal(source_price.price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        return None

    if price <= 0:
        return None

    currency = source_price.currency.strip().upper()
    if not currency:
        return None

    return NormalizedPrice(
        product_id=source_price.product_id,
        store=source_price.store,
        price=price,
        currency=currency,
    )

