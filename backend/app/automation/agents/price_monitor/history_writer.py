from sqlalchemy.orm import Session

from app.models.price_history import PriceHistory


def write_price_history(
    db: Session,
    *,
    product_id: int,
    store_id: int,
    price: object,
) -> PriceHistory:
    history = PriceHistory(product_id=product_id, store_id=store_id, price=price)
    db.add(history)
    db.flush()
    return history

