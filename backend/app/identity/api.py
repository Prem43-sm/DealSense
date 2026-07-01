from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.identity.service import IdentityMappingService

router = APIRouter(prefix="/identity", tags=["identity"])


class ProductSourceRead(BaseModel):
    source: str
    external_id: str
    product_url: str | None = None
    canonical_url: str | None = None
    active: bool


class IdentityProductRead(BaseModel):
    id: int
    title: str
    brand: str | None = None
    category: str | None = None
    sources: list[ProductSourceRead]


@router.get("/products", response_model=list[IdentityProductRead])
def list_identity_products(db: Session = Depends(get_db)) -> list[IdentityProductRead]:
    service = IdentityMappingService(db)
    products = service.list_products()
    return [
        IdentityProductRead(
            id=product.id,
            title=product.title,
            brand=product.brand,
            category=product.category,
            sources=[
                ProductSourceRead(
                    source=source.source_name,
                    external_id=source.external_product_id,
                    product_url=source.product_url,
                    canonical_url=source.canonical_url,
                    active=source.active,
                )
                for source in product.sources
            ],
        )
        for product in products
    ]

