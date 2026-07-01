from fastapi import APIRouter, Depends

from app.automation.common.scheduler import AutomationScheduler
from app.automation.services.health_service import HealthService, get_health_service

router = APIRouter(prefix="/automation", tags=["automation"])


@router.get("/status")
def automation_status(
    health_service: HealthService = Depends(get_health_service),
) -> dict[str, object]:
    return health_service.status()


@router.get("/product-discovery/run")
def run_product_discovery() -> dict[str, object]:
    scheduler = AutomationScheduler()
    agents = scheduler.register_all_agents()
    product_discovery = next(agent for agent in agents if agent.name == "product_discovery")
    summary = product_discovery.run()
    return {"status": "success", "summary": summary.model_dump()}


@router.get("/price-monitor/run")
def run_price_monitor() -> dict[str, object]:
    scheduler = AutomationScheduler()
    agents = scheduler.register_all_agents()
    price_monitor = next(agent for agent in agents if agent.name == "price_monitor")
    summary = price_monitor.run()
    return {
        "status": "success",
        "summary": summary.model_dump(
            include={"products_checked", "prices_updated", "unchanged", "failed"}
        ),
    }
