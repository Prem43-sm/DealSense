from app.automation.agents.product_discovery.config import get_config
from app.automation.common.base_agent import BaseAgent


class ProductDiscoveryAgent(BaseAgent):
    name = "product_discovery"
    config_factory = staticmethod(get_config)

    def run(self) -> None:
        self.log("Product discovery agent is ready")

