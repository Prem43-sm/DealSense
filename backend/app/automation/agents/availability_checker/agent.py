from time import perf_counter

from app.automation.agents.availability_checker.config import get_config
from app.automation.agents.availability_checker.service import AvailabilityCheckerService, AvailabilitySummary
from app.automation.common.base_agent import BaseAgent


class AvailabilityCheckerAgent(BaseAgent):
    name = "availability_checker"
    config_factory = staticmethod(get_config)

    def run(self) -> AvailabilitySummary:
        started_at = perf_counter()
        self.log("Availability Checker Started")

        database_service = self.runtime.services["database"]
        with database_service.session() as db:
            service = AvailabilityCheckerService(db, logger=self.runtime.logger)
            summary = service.check_availability()

        duration_seconds = round(perf_counter() - started_at, 2)
        self.log(
            "Availability Checker Finished",
            duration_seconds=duration_seconds,
            checked=summary.checked,
            updated=summary.updated,
            unchanged=summary.unchanged,
            failed=summary.failed,
        )
        return summary
