from app.automation.common.scheduler import AutomationScheduler
from app.automation.agents.product_discovery.service import ProductDiscoveryStateStore
from app.automation.agents.price_monitor.service import PriceMonitorStateStore
from app.automation.agents.affiliate_manager.service import AffiliateManagerStateStore
from app.automation.services.database_service import DatabaseService
from app.identity.service import IdentityMappingService


class HealthService:
    def __init__(
        self,
        scheduler: AutomationScheduler,
        product_discovery_state_store: ProductDiscoveryStateStore | None = None,
        price_monitor_state_store: PriceMonitorStateStore | None = None,
        affiliate_manager_state_store: AffiliateManagerStateStore | None = None,
        database_service: DatabaseService | None = None,
    ) -> None:
        self.scheduler = scheduler
        self.agents = scheduler.register_all_agents()
        self.product_discovery_state_store = product_discovery_state_store or ProductDiscoveryStateStore()
        self.price_monitor_state_store = price_monitor_state_store or PriceMonitorStateStore()
        self.affiliate_manager_state_store = affiliate_manager_state_store or AffiliateManagerStateStore()
        self.database_service = database_service or DatabaseService()

    def status(self) -> dict[str, object]:
        return {
            "framework": "ready",
            "scheduler": self.scheduler.status(),
            "identity_system": self._identity_health(),
            "agents": [self._agent_health(agent.health()) for agent in self.agents],
        }

    def _identity_health(self) -> dict[str, object]:
        with self.database_service.session() as db:
            state = IdentityMappingService(db).health()
            return {
                "status": state.status,
                "mapped_products": state.mapped_products,
                "new_products": state.new_products,
                "duplicate_prevented": state.duplicate_prevented,
            }

    def _agent_health(self, health: dict[str, str]) -> dict[str, object]:
        if health["name"] == "product_discovery":
            state = self.product_discovery_state_store.read()
            return {
                **health,
                "last_run": state.last_run,
                "products_discovered": state.products_discovered,
                "duplicates_found": state.duplicates_found,
                "status": state.status,
            }

        if health["name"] == "price_monitor":
            state = self.price_monitor_state_store.read()
            return {
                **health,
                "last_run": state.last_run,
                "products_checked": state.products_checked,
                "prices_updated": state.prices_updated,
                "status": state.status,
            }

        if health["name"] == "affiliate_manager":
            state = self.affiliate_manager_state_store.read()
            return {
                **health,
                "last_run": state.last_run,
                "links_generated": state.links_generated,
                "validation_status": state.validation_status,
                "status": state.status,
            }

        return health


def get_health_service() -> HealthService:
    return HealthService(AutomationScheduler())
