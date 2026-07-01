from datetime import UTC, datetime
from enum import StrEnum

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.identity.matcher import ProductMatcher
from app.identity.normalizer import NormalizedMarketplaceProduct
from app.models.product import Product
from app.models.product_source import ProductSource


class MappingStatus(StrEnum):
    CREATED_PRODUCT = "created_product"
    CREATED_MAPPING = "created_mapping"
    EXISTING_MAPPING = "existing_mapping"


class ProductIdentityMapper:
    def __init__(self, db: Session, matcher: ProductMatcher | None = None) -> None:
        self.db = db
        self.matcher = matcher or ProductMatcher(db)

    def map_product(self, incoming: NormalizedMarketplaceProduct) -> tuple[Product, ProductSource, MappingStatus]:
        existing_mapping = self._find_mapping(incoming)
        if existing_mapping:
            existing_mapping.last_seen = datetime.now(UTC)
            existing_mapping.active = True
            return existing_mapping.product, existing_mapping, MappingStatus.EXISTING_MAPPING

        product = self.matcher.find_match(incoming)
        status = MappingStatus.CREATED_MAPPING
        if product is None:
            product = self._create_master_product(incoming)
            status = MappingStatus.CREATED_PRODUCT

        mapping = ProductSource(
            product_id=product.id,
            source_name=incoming.source_name,
            external_product_id=incoming.external_product_id,
            product_url=incoming.product_url,
            canonical_url=incoming.canonical_url,
            active=True,
        )
        self.db.add(mapping)
        self.db.flush()
        return product, mapping, status

    def _find_mapping(self, incoming: NormalizedMarketplaceProduct) -> ProductSource | None:
        return self.db.scalar(
            select(ProductSource).where(
                ProductSource.source_name == incoming.source_name,
                ProductSource.external_product_id == incoming.external_product_id,
            )
        )

    def _create_master_product(self, incoming: NormalizedMarketplaceProduct) -> Product:
        product = Product(
            title=incoming.title,
            slug=incoming.slug,
            brand=incoming.brand,
            category=incoming.category,
            image_url=incoming.image_url,
            description=incoming.description,
        )
        self.db.add(product)
        self.db.flush()
        return product

