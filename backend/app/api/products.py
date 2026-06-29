import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.database.connection import get_db
from app.models.price import Price
from app.models.product import Product
from app.schemas.product import ProductDetail, ProductRead

logger = logging.getLogger(__name__)
router = APIRouter(tags=["products"])


@router.get("/products", response_model=list[ProductRead])
def list_products(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[Product]:
    offset = (page - 1) * limit
    logger.info("Listing products", extra={"_page": page, "_limit": limit})
    return list(
        db.scalars(
            select(Product)
            .order_by(Product.created_at.desc(), Product.id.desc())
            .offset(offset)
            .limit(limit)
        )
    )


@router.get("/products/{product_id}", response_model=ProductDetail)
def get_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    product = db.scalar(
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.prices).selectinload(Price.store))
    )
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/search", response_model=list[ProductRead])
def search_products(
    q: str = Query(min_length=1),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[Product]:
    offset = (page - 1) * limit
    normalized_query = f"%{q.strip().lower()}%"
    logger.info("Searching products", extra={"_query": q, "_page": page, "_limit": limit})
    return list(
        db.scalars(
            select(Product)
            .where(
                or_(
                    func.lower(Product.title).like(normalized_query),
                    func.lower(Product.brand).like(normalized_query),
                    func.lower(Product.category).like(normalized_query),
                )
            )
            .order_by(Product.created_at.desc(), Product.id.desc())
            .offset(offset)
            .limit(limit)
        )
    )
