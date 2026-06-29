from app.automation.agents.affiliate_manager.config import get_config
from app.automation.common.base_agent import BaseAgent


class AffiliateManagerAgent(BaseAgent):
    name = "affiliate_manager"
    config_factory = staticmethod(get_config)

    def run(self) -> None:
        self.log("Affiliate manager agent is ready")

