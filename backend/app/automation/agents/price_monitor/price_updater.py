from sqlalchemy import select
from sqlalchemy.orm import Session

from app.automation.agents.price_monitor.price_normalizer import NormalizedPrice
from app.models.price import Price
from app.services.price_service import get_or_create_store


def get_current_price(db: Session, product_id: int, store_name: str) -> Price | None:
    return db.scalar(
        select(Price)
        .join(Price.store)
        .where(
            Price.product_id == product_id,
            Price.store.has(name=store_name),
        )
    )


def update_current_price(
    db: Session,
    normalized_price: NormalizedPrice,
    current_price: Price | None,
) -> Price:
    store = get_or_create_store(db, name=normalized_price.store)
    if current_price is None:
        current_price = Price(
            product_id=normalized_price.product_id,
            store_id=store.id,
            current_price=normalized_price.price,
            availability=True,
            affiliate_url="https://example.com/price-monitor",
        )
        db.add(current_price)
        db.flush()
        return current_price

    current_price.current_price = normalized_price.price
    db.flush()
    return current_price

