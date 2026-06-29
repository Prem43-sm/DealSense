from app.automation.agents.shopping_assistant.config import get_config
from app.automation.common.base_agent import BaseAgent


class ShoppingAssistantAgent(BaseAgent):
    name = "shopping_assistant"
    config_factory = staticmethod(get_config)

    def run(self) -> None:
        self.log("Shopping assistant agent is ready")

