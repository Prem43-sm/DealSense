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


@router.get("/affiliate-manager/run")
def run_affiliate_manager() -> dict[str, object]:
    scheduler = AutomationScheduler()
    agents = scheduler.register_all_agents()
    affiliate_manager = next(agent for agent in agents if agent.name == "affiliate_manager")
    summary = affiliate_manager.run()
    return {
        "status": "success",
        "summary": summary.model_dump(
            include={"sources_checked", "links_generated", "duplicates", "failed"}
        ),
    }


@router.get("/availability/run")
def run_availability_checker() -> dict[str, object]:
    scheduler = AutomationScheduler()
    agents = scheduler.register_all_agents()
    availability_checker = next(agent for agent in agents if agent.name == "availability_checker")
    summary = availability_checker.run()
    return {"status": "success", "summary": summary.model_dump()}
