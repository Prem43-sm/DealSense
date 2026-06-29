from app.automation.agents.availability_checker.config import get_config
from app.automation.common.base_agent import BaseAgent


class AvailabilityCheckerAgent(BaseAgent):
    name = "availability_checker"
    config_factory = staticmethod(get_config)

    def run(self) -> None:
        self.log("Availability checker agent is ready")

