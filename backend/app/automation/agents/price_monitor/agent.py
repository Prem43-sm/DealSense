from time import perf_counter

from app.automation.agents.price_monitor.config import get_config
from app.automation.agents.price_monitor.service import PriceMonitorService, PriceMonitorSummary
from app.automation.common.base_agent import BaseAgent


class PriceMonitorAgent(BaseAgent):
    name = "price_monitor"
    config_factory = staticmethod(get_config)

    def run(self) -> PriceMonitorSummary:
        started_at = perf_counter()
        self.log("Price Monitor Started")

        database_service = self.runtime.services["database"]
        with database_service.session() as db:
            service = PriceMonitorService(db, logger=self.runtime.logger)
            summary = service.monitor_prices()

        duration_seconds = round(perf_counter() - started_at, 2)
        self.log(
            "Price Monitor Finished",
            duration_seconds=duration_seconds,
            products_checked=summary.products_checked,
            prices_updated=summary.prices_updated,
            history_entries=summary.history_entries,
            failed=summary.failed,
        )
        return summary
