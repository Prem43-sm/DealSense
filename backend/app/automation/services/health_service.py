from app.automation.common.scheduler import AutomationScheduler
from app.automation.agents.product_discovery.service import ProductDiscoveryStateStore


class HealthService:
    def __init__(
        self,
        scheduler: AutomationScheduler,
        product_discovery_state_store: ProductDiscoveryStateStore | None = None,
    ) -> None:
        self.scheduler = scheduler
        self.agents = scheduler.register_all_agents()
        self.product_discovery_state_store = product_discovery_state_store or ProductDiscoveryStateStore()

    def status(self) -> dict[str, object]:
        return {
            "framework": "ready",
            "scheduler": self.scheduler.status(),
            "agents": [self._agent_health(agent.health()) for agent in self.agents],
        }

    def _agent_health(self, health: dict[str, str]) -> dict[str, object]:
        if health["name"] != "product_discovery":
            return health

        state = self.product_discovery_state_store.read()
        return {
            **health,
            "last_run": state.last_run,
            "products_discovered": state.products_discovered,
            "duplicates_found": state.duplicates_found,
            "status": state.status,
        }


def get_health_service() -> HealthService:
    return HealthService(AutomationScheduler())
