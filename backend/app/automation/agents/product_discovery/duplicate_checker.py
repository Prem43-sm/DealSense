from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.automation.agents.product_discovery.normalizer import NormalizedProduct
from app.models.product import Product


class DuplicateChecker:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.seen_external_ids: set[str] = set()

    def is_duplicate(self, product: NormalizedProduct) -> bool:
        if product.external_id:
            if product.external_id in self.seen_external_ids:
                return True
            self.seen_external_ids.add(product.external_id)

        existing = self.db.scalar(
            select(Product.id).where(
                or_(
                    func.lower(Product.title) == product.title.lower(),
                    Product.slug == product.slug,
                )
            )
        )
        return existing is not None

