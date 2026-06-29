from app.automation.agents.price_monitor.config import get_config
from app.automation.common.base_agent import BaseAgent


class PriceMonitorAgent(BaseAgent):
    name = "price_monitor"
    config_factory = staticmethod(get_config)

    def run(self) -> None:
        self.log("Price monitor agent is ready")

