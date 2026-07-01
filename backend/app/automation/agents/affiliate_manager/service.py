import json
import logging
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.automation.agents.affiliate_manager.generator import AffiliateGenerator
from app.automation.agents.affiliate_manager.repository import AffiliateLinkRepository
from app.automation.agents.affiliate_manager.validator import AffiliateLinkValidator


class AffiliateManagerSummary(BaseModel):
    sources_checked: int = 0
    links_generated: int = 0
    duplicates: int = 0
    failed: int = 0
    validation_status: str = "UNKNOWN"


class AffiliateManagerState(BaseModel):
    last_run: str | None = None
    links_generated: int = 0
    validation_status: str = "UNKNOWN"
    status: str = "ready"


class AffiliateManagerStateStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path(__file__).resolve().parents[2] / "logs" / "affiliate_manager_state.json"

    def read(self) -> AffiliateManagerState:
        if not self.path.exists():
            return AffiliateManagerState()
        return AffiliateManagerState.model_validate_json(self.path.read_text(encoding="utf-8"))

    def write(self, state: AffiliateManagerState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(state.model_dump(), indent=2), encoding="utf-8")


class AffiliateManagerService:
    def __init__(
        self,
        db: Session,
        repository: AffiliateLinkRepository | None = None,
        generator: AffiliateGenerator | None = None,
        validator: AffiliateLinkValidator | None = None,
        state_store: AffiliateManagerStateStore | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.db = db
        self.repository = repository or AffiliateLinkRepository(db)
        self.generator = generator or AffiliateGenerator()
        self.validator = validator or AffiliateLinkValidator()
        self.state_store = state_store or AffiliateManagerStateStore()
        self.logger = logger

    def generate_affiliate_links(self) -> AffiliateManagerSummary:
        summary = AffiliateManagerSummary()
        try:
            for product_source in self.repository.list_product_sources():
                summary.sources_checked += 1
                generated = self.generator.generate(product_source)
                if generated is None:
                    summary.failed += 1
                    self._log("Affiliate generation failed", source_id=product_source.id)
                    continue

                status = self.validator.validate(provider=generated.provider, url=generated.url)
                link, created = self.repository.save_link(
                    product_source_id=product_source.id,
                    provider=generated.provider,
                    affiliate_url=generated.url,
                    status=status.value,
                    tracking_id=self._tracking_id(product_source.source_name),
                )
                summary.validation_status = status.value

                if not created:
                    summary.duplicates += 1
                    self._log(
                        "Duplicate affiliate link updated",
                        source_id=product_source.id,
                        provider=link.provider,
                        status=status.value,
                    )
                    continue

                summary.links_generated += 1
                self._log(
                    "Affiliate link generated",
                    source_id=product_source.id,
                    provider=link.provider,
                    status=status.value,
                )

            self.db.commit()
            self._write_state(summary, "ready")
            return summary
        except Exception:
            self.db.rollback()
            self._write_state(summary, "error")
            raise

    def _write_state(self, summary: AffiliateManagerSummary, status: str) -> None:
        self.state_store.write(
            AffiliateManagerState(
                last_run=datetime.now(UTC).isoformat(),
                links_generated=summary.links_generated,
                validation_status=summary.validation_status,
                status=status,
            )
        )

    def _tracking_id(self, provider: str) -> str:
        if provider.lower() == "amazon":
            return "dealsenseprem-21"
        if provider.lower() == "flipkart":
            return "dealsense"
        return f"dealsense-{provider.lower()}"

    def _log(self, message: str, **extra: object) -> None:
        if self.logger is None:
            return
        self.logger.info(message, extra={f"_{key}": value for key, value in extra.items()})
