import json
import logging
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.automation.agents.product_discovery.duplicate_checker import DuplicateChecker
from app.automation.agents.product_discovery.normalizer import normalize_product
from app.automation.agents.product_discovery.product_mapper import map_to_product
from app.automation.agents.product_discovery.sources import ProductSource, get_product_sources
from app.automation.agents.product_discovery.validator import validate_source_product


class DiscoverySummary(BaseModel):
    fetched: int = 0
    inserted: int = 0
    duplicates: int = 0
    failed: int = 0


class ProductDiscoveryState(BaseModel):
    last_run: str | None = None
    products_discovered: int = 0
    duplicates_found: int = 0
    status: str = "ready"


class ProductDiscoveryStateStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path(__file__).resolve().parents[2] / "logs" / "product_discovery_state.json"

    def read(self) -> ProductDiscoveryState:
        if not self.path.exists():
            return ProductDiscoveryState()
        return ProductDiscoveryState.model_validate_json(self.path.read_text(encoding="utf-8"))

    def write(self, state: ProductDiscoveryState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(state.model_dump(), indent=2), encoding="utf-8")


class ProductDiscoveryService:
    def __init__(
        self,
        db: Session,
        sources: list[ProductSource] | None = None,
        state_store: ProductDiscoveryStateStore | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.db = db
        self.sources = sources or get_product_sources()
        self.state_store = state_store or ProductDiscoveryStateStore()
        self.logger = logger

    def discover_products(self) -> DiscoverySummary:
        summary = DiscoverySummary()
        duplicate_checker = DuplicateChecker(self.db)

        try:
            for source in self.sources:
                self._log("Discovery source started", source=source.name)
                source_products = source.fetch_products()
                summary.fetched += len(source_products)
                self._log("Fetched products", source=source.name, fetched=len(source_products))

                for source_product in source_products:
                    try:
                        if not validate_source_product(source_product):
                            summary.failed += 1
                            continue

                        product = normalize_product(source_product)
                        if duplicate_checker.is_duplicate(product):
                            summary.duplicates += 1
                            continue

                        self.db.add(map_to_product(product))
                        summary.inserted += 1
                    except Exception:
                        summary.failed += 1

            self.db.commit()
            self._write_state(summary, "ready")
            self._log(
                "Discovery summary",
                fetched=summary.fetched,
                inserted=summary.inserted,
                duplicates=summary.duplicates,
                failed=summary.failed,
            )
            return summary
        except Exception:
            self.db.rollback()
            self._write_state(summary, "error")
            raise

    def _write_state(self, summary: DiscoverySummary, status: str) -> None:
        self.state_store.write(
            ProductDiscoveryState(
                last_run=datetime.now(UTC).isoformat(),
                products_discovered=summary.inserted,
                duplicates_found=summary.duplicates,
                status=status,
            )
        )

    def _log(self, message: str, **extra: object) -> None:
        if self.logger is None:
            return
        self.logger.info(message, extra={f"_{key}": value for key, value in extra.items()})
