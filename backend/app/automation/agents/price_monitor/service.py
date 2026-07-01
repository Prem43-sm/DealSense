import json
import logging
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.automation.agents.price_monitor.history_writer import write_price_history
from app.automation.agents.price_monitor.price_comparator import compare_price
from app.automation.agents.price_monitor.price_normalizer import normalize_price
from app.automation.agents.price_monitor.price_updater import get_current_price, update_current_price
from app.automation.agents.price_monitor.sources import PriceSource, get_price_sources
from app.models.product_source import ProductSource as MarketplaceProductSource
from app.services.deal_service import create_deal_if_discounted


class PriceMonitorSummary(BaseModel):
    products_checked: int = 0
    prices_updated: int = 0
    unchanged: int = 0
    failed: int = 0
    history_entries: int = 0


class PriceMonitorState(BaseModel):
    last_run: str | None = None
    products_checked: int = 0
    prices_updated: int = 0
    status: str = "ready"


class PriceMonitorStateStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path(__file__).resolve().parents[2] / "logs" / "price_monitor_state.json"

    def read(self) -> PriceMonitorState:
        if not self.path.exists():
            return PriceMonitorState()
        return PriceMonitorState.model_validate_json(self.path.read_text(encoding="utf-8"))

    def write(self, state: PriceMonitorState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(state.model_dump(), indent=2), encoding="utf-8")


class PriceMonitorService:
    def __init__(
        self,
        db: Session,
        sources: list[PriceSource] | None = None,
        state_store: PriceMonitorStateStore | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.db = db
        self.sources = sources or get_price_sources()
        self.state_store = state_store or PriceMonitorStateStore()
        self.logger = logger

    def monitor_prices(self) -> PriceMonitorSummary:
        summary = PriceMonitorSummary()
        product_sources = list(
            self.db.scalars(
                select(MarketplaceProductSource)
                .where(MarketplaceProductSource.active.is_(True))
                .options(selectinload(MarketplaceProductSource.product))
                .order_by(MarketplaceProductSource.id)
            )
        )

        try:
            for source in self.sources:
                self._log("Price source started", source=source.name)
                source.start_run()
                for product_source in product_sources:
                    self._check_product(source, product_source, summary)
                source.finish_run()

            self.db.commit()
            self._write_state(summary, "ready")
            self._log(
                "Price monitor summary",
                products_checked=summary.products_checked,
                prices_updated=summary.prices_updated,
                unchanged=summary.unchanged,
                failed=summary.failed,
                history_entries=summary.history_entries,
            )
            return summary
        except Exception:
            self.db.rollback()
            self._write_state(summary, "error")
            raise

    def _check_product(
        self,
        source: PriceSource,
        product_source: MarketplaceProductSource,
        summary: PriceMonitorSummary,
    ) -> None:
        try:
            source_price = source.fetch_price(product_source)
            if source_price is None:
                return

            summary.products_checked += 1
            normalized_price = normalize_price(source_price)
            if normalized_price is None:
                summary.failed += 1
                return

            current_price = get_current_price(self.db, product_source.product_id, normalized_price.store)
            old_price = current_price.current_price if current_price else None
            comparison = compare_price(old_price, normalized_price.price)

            if not comparison.price_changed:
                summary.unchanged += 1
                return

            updated_price = update_current_price(self.db, normalized_price, current_price)
            write_price_history(
                self.db,
                product_id=product_source.product_id,
                store_id=updated_price.store_id,
                price=normalized_price.price,
            )
            summary.prices_updated += 1
            summary.history_entries += 1

            if comparison.old_price is not None:
                create_deal_if_discounted(
                    self.db,
                    product_id=product_source.product_id,
                    old_price=comparison.old_price,
                    new_price=comparison.new_price,
                )
        except Exception:
            summary.failed += 1
            self._log(
                "Price monitor product failed",
                product_id=product_source.product_id,
                source_id=product_source.id,
            )

    def _write_state(self, summary: PriceMonitorSummary, status: str) -> None:
        self.state_store.write(
            PriceMonitorState(
                last_run=datetime.now(UTC).isoformat(),
                products_checked=summary.products_checked,
                prices_updated=summary.prices_updated,
                status=status,
            )
        )

    def _log(self, message: str, **extra: object) -> None:
        if self.logger is None:
            return
        self.logger.info(message, extra={f"_{key}": value for key, value in extra.items()})
