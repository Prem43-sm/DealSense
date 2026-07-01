import json
import logging
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.automation.agents.availability_checker.checker import AvailabilityChecker
from app.automation.agents.availability_checker.repository import AvailabilityRepository


class AvailabilitySummary(BaseModel):
    checked: int = 0
    updated: int = 0
    unchanged: int = 0
    failed: int = 0


class AvailabilityCheckerState(BaseModel):
    last_run: str | None = None
    checked: int = 0
    updated: int = 0
    status: str = "ready"


class AvailabilityCheckerStateStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path(__file__).resolve().parents[2] / "logs" / "availability_checker_state.json"

    def read(self) -> AvailabilityCheckerState:
        if not self.path.exists():
            return AvailabilityCheckerState()
        return AvailabilityCheckerState.model_validate_json(self.path.read_text(encoding="utf-8"))

    def write(self, state: AvailabilityCheckerState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(state.model_dump(), indent=2), encoding="utf-8")


class AvailabilityCheckerService:
    def __init__(
        self,
        db: Session,
        repository: AvailabilityRepository | None = None,
        checker: AvailabilityChecker | None = None,
        state_store: AvailabilityCheckerStateStore | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.db = db
        self.repository = repository or AvailabilityRepository(db)
        self.checker = checker or AvailabilityChecker()
        self.state_store = state_store or AvailabilityCheckerStateStore()
        self.logger = logger

    def check_availability(self) -> AvailabilitySummary:
        summary = AvailabilitySummary()
        try:
            for product_source in self.repository.list_product_sources():
                availability = self.checker.check(product_source)
                if availability is None:
                    summary.failed += 1
                    self._log("Availability check failed", source_id=product_source.id)
                    continue

                summary.checked += 1
                old = self.repository.get_status(product_source.id, availability.provider)
                record, changed = self.repository.save_status(
                    product_source_id=product_source.id,
                    provider=availability.provider,
                    status=availability.status.value,
                    quantity=availability.quantity,
                )
                if changed:
                    summary.updated += 1
                else:
                    summary.unchanged += 1

                self._log(
                    "Availability checked",
                    source_id=product_source.id,
                    provider=record.provider,
                    old_status=old.status if old else None,
                    new_status=record.status,
                )

            self.db.commit()
            self._write_state(summary, "ready")
            return summary
        except Exception:
            self.db.rollback()
            self._write_state(summary, "error")
            raise

    def _write_state(self, summary: AvailabilitySummary, status: str) -> None:
        self.state_store.write(
            AvailabilityCheckerState(
                last_run=datetime.now(UTC).isoformat(),
                checked=summary.checked,
                updated=summary.updated,
                status=status,
            )
        )

    def _log(self, message: str, **extra: object) -> None:
        if self.logger is None:
            return
        self.logger.info(message, extra={f"_{key}": value for key, value in extra.items()})

