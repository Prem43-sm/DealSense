from app.automation.agents.content_generator.config import get_config
from app.automation.common.base_agent import BaseAgent


class ContentGeneratorAgent(BaseAgent):
    name = "content_generator"
    config_factory = staticmethod(get_config)

    def run(self) -> None:
        self.log("Content generator agent is ready")

