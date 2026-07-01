import json
import logging
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.identity.mapper import MappingStatus, ProductIdentityMapper
from app.identity.normalizer import IncomingMarketplaceProduct, normalize_marketplace_product
from app.identity.logger import get_identity_logger
from app.models.product import Product
from app.models.product_source import ProductSource


class ProductMappingResult(BaseModel):
    product_id: int
    source_id: int
    status: MappingStatus


class IdentityState(BaseModel):
    status: str = "ready"
    mapped_products: int = 0
    new_products: int = 0
    duplicate_prevented: int = 0
    last_run: str | None = None


class IdentityStateStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path(__file__).resolve().parents[1] / "automation" / "logs" / "identity_state.json"

    def read(self) -> IdentityState:
        if not self.path.exists():
            return IdentityState()
        return IdentityState.model_validate_json(self.path.read_text(encoding="utf-8"))

    def write(self, state: IdentityState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(state.model_dump(), indent=2), encoding="utf-8")


class IdentityMappingService:
    def __init__(
        self,
        db: Session,
        logger: logging.Logger | None = None,
        state_store: IdentityStateStore | None = None,
    ) -> None:
        self.db = db
        self.logger = logger or get_identity_logger()
        self.state_store = state_store or IdentityStateStore()
        self.mapper = ProductIdentityMapper(db)

    def map_product(self, product: IncomingMarketplaceProduct) -> ProductMappingResult:
        normalized = normalize_marketplace_product(product)
        master_product, mapping, status = self.mapper.map_product(normalized)
        self._update_state(status)
        self._log_mapping(master_product, mapping, status)
        return ProductMappingResult(product_id=master_product.id, source_id=mapping.id, status=status)

    def list_products(self) -> list[Product]:
        return list(
            self.db.scalars(
                select(Product)
                .options(selectinload(Product.sources))
                .order_by(Product.created_at.desc(), Product.id.desc())
            )
        )

    def health(self) -> IdentityState:
        mapped_products = self.db.scalar(select(func.count(ProductSource.id))) or 0
        current = self.state_store.read()
        return IdentityState(
            status=current.status,
            mapped_products=mapped_products,
            new_products=current.new_products,
            duplicate_prevented=current.duplicate_prevented,
            last_run=current.last_run,
        )

    def _update_state(self, status: MappingStatus) -> None:
        current = self.state_store.read()
        current.status = "ready"
        current.last_run = datetime.now(UTC).isoformat()
        if status == MappingStatus.CREATED_PRODUCT:
            current.new_products += 1
        elif status == MappingStatus.EXISTING_MAPPING:
            current.duplicate_prevented += 1
        self.state_store.write(current)

    def _log_mapping(self, product: Product, mapping: ProductSource, status: MappingStatus) -> None:
        if self.logger is None:
            return
        messages = {
            MappingStatus.CREATED_PRODUCT: "New master product",
            MappingStatus.CREATED_MAPPING: "New mapping created",
            MappingStatus.EXISTING_MAPPING: "Duplicate prevented",
        }
        self.logger.info(
            messages[status],
            extra={
                "_product_id": product.id,
                "_source": mapping.source_name,
                "_external_id": mapping.external_product_id,
                "_status": status.value,
            },
        )
