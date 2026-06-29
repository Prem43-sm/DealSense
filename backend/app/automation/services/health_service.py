from app.automation.common.scheduler import AutomationScheduler


class HealthService:
    def __init__(self, scheduler: AutomationScheduler) -> None:
        self.scheduler = scheduler
        self.agents = scheduler.register_all_agents()

    def status(self) -> dict[str, object]:
        return {
            "framework": "ready",
            "scheduler": self.scheduler.status(),
            "agents": [agent.health() for agent in self.agents],
        }


def get_health_service() -> HealthService:
    return HealthService(AutomationScheduler())

