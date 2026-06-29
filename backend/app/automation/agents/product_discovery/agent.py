from time import perf_counter

from app.automation.agents.product_discovery.config import get_config
from app.automation.agents.product_discovery.service import DiscoverySummary, ProductDiscoveryService
from app.automation.common.base_agent import BaseAgent


class ProductDiscoveryAgent(BaseAgent):
    name = "product_discovery"
    config_factory = staticmethod(get_config)

    def run(self) -> DiscoverySummary:
        started_at = perf_counter()
        self.log("Discovery Started")

        database_service = self.runtime.services["database"]
        with database_service.session() as db:
            service = ProductDiscoveryService(db, logger=self.runtime.logger)
            summary = service.discover_products()

        duration_seconds = round(perf_counter() - started_at, 2)
        self.log(
            "Discovery Finished",
            duration_seconds=duration_seconds,
            inserted=summary.inserted,
            duplicates=summary.duplicates,
            failed=summary.failed,
        )
        return summary
