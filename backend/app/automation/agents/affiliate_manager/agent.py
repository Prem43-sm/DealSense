from time import perf_counter

from app.automation.agents.affiliate_manager.config import get_config
from app.automation.agents.affiliate_manager.service import AffiliateManagerService, AffiliateManagerSummary
from app.automation.common.base_agent import BaseAgent


class AffiliateManagerAgent(BaseAgent):
    name = "affiliate_manager"
    config_factory = staticmethod(get_config)

    def run(self) -> AffiliateManagerSummary:
        started_at = perf_counter()
        self.log("Affiliate Manager Started")

        database_service = self.runtime.services["database"]
        with database_service.session() as db:
            service = AffiliateManagerService(db, logger=self.runtime.logger)
            summary = service.generate_affiliate_links()

        duration_seconds = round(perf_counter() - started_at, 2)
        self.log(
            "Affiliate Manager Finished",
            duration_seconds=duration_seconds,
            sources_checked=summary.sources_checked,
            links_generated=summary.links_generated,
            duplicates=summary.duplicates,
            failed=summary.failed,
        )
        return summary
