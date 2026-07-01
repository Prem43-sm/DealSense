from difflib import SequenceMatcher

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.identity.normalizer import NormalizedMarketplaceProduct, normalize_for_match
from app.models.product import Product
from app.models.product_source import ProductSource


class ProductMatcher:
    def __init__(self, db: Session, similarity_threshold: float = 0.88) -> None:
        self.db = db
        self.similarity_threshold = similarity_threshold

    def find_match(self, incoming: NormalizedMarketplaceProduct) -> Product | None:
        mapped_product = self._match_external_mapping(incoming)
        if mapped_product:
            return mapped_product

        slug_match = self.db.scalar(select(Product).where(Product.slug == incoming.slug))
        if slug_match:
            return slug_match

        title_match = self.db.scalar(
            select(Product).where(func.lower(Product.title) == incoming.title.lower())
        )
        if title_match:
            return title_match

        return self._match_brand_title_similarity(incoming)

    def _match_external_mapping(self, incoming: NormalizedMarketplaceProduct) -> Product | None:
        mapping = self.db.scalar(
            select(ProductSource)
            .where(
                ProductSource.source_name == incoming.source_name,
                ProductSource.external_product_id == incoming.external_product_id,
            )
            .limit(1)
        )
        return mapping.product if mapping else None

    def _match_brand_title_similarity(self, incoming: NormalizedMarketplaceProduct) -> Product | None:
        if not incoming.brand:
            return None

        candidates = list(
            self.db.scalars(select(Product).where(func.lower(Product.brand) == incoming.brand.lower()))
        )
        best_product: Product | None = None
        best_score = 0.0
        for product in candidates:
            score = SequenceMatcher(
                None,
                normalize_for_match(product.title),
                incoming.normalized_title,
            ).ratio()
            if score > best_score:
                best_score = score
                best_product = product

        if best_score >= self.similarity_threshold:
            return best_product
        return None

