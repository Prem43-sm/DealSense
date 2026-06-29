import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database.connection import get_db
from app.models.price import Price
from app.models.price_history import PriceHistory
from app.models.product import Product
from app.schemas.price import PriceHistoryRead
from app.schemas.product import ProductPriceRead

logger = logging.getLogger(__name__)
router = APIRouter(tags=["prices"])


def ensure_product_exists(db: Session, product_id: int) -> None:
    exists = db.scalar(select(Product.id).where(Product.id == product_id))
    if exists is None:
        raise HTTPException(status_code=404, detail="Product not found")


@router.get("/products/{product_id}/prices", response_model=list[ProductPriceRead])
def get_product_prices(product_id: int, db: Session = Depends(get_db)) -> list[Price]:
    ensure_product_exists(db, product_id)
    logger.info("Fetching product prices", extra={"_product_id": product_id})
    return list(
        db.scalars(
            select(Price)
            .where(Price.product_id == product_id)
            .options(joinedload(Price.store))
            .order_by(Price.current_price.asc())
        )
    )


@router.get("/products/{product_id}/history", response_model=list[PriceHistoryRead])
def get_product_history(
    product_id: int,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[PriceHistory]:
    ensure_product_exists(db, product_id)
    offset = (page - 1) * limit
    logger.info(
        "Fetching product price history",
        extra={"_product_id": product_id, "_page": page, "_limit": limit},
    )
    return list(
        db.scalars(
            select(PriceHistory)
            .where(PriceHistory.product_id == product_id)
            .order_by(PriceHistory.created_at.desc(), PriceHistory.id.desc())
            .offset(offset)
            .limit(limit)
        )
    )
