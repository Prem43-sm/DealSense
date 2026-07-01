from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.automation.agents.affiliate_manager.repository import AffiliateLinkRepository
from app.automation.agents.affiliate_manager.service import AffiliateManagerStateStore
from app.automation.agents.availability_checker.repository import AvailabilityRepository
from app.automation.agents.availability_checker.service import AvailabilityCheckerStateStore
from app.automation.agents.price_monitor.service import PriceMonitorStateStore
from app.automation.agents.product_discovery.service import ProductDiscoveryStateStore
from app.connectors.manager import ConnectorManager
from app.identity.service import IdentityMappingService
from app.models.affiliate_link import AffiliateLink
from app.models.availability_status import AvailabilityStatus
from app.models.deal import Deal
from app.models.price import Price
from app.models.product import Product
from app.models.product_source import ProductSource


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def summary(self) -> dict[str, Any]:
        connectors = ConnectorManager().health_checks()
        return {
            "products": self._count(Product.id),
            "price_records": self._count(Price.id),
            "affiliate_links": self._count(AffiliateLink.id),
            "availability_records": self._count(AvailabilityStatus.id),
            "deals": self._count(Deal.id),
            "connector_health": self._healthy_count(connectors),
            "automation_health": "ready",
            "recent_logs": self.recent_logs(),
        }

    def automation(self) -> dict[str, Any]:
        product_discovery = ProductDiscoveryStateStore().read()
        price_monitor = PriceMonitorStateStore().read()
        affiliate_manager = AffiliateManagerStateStore().read()
        availability_checker = AvailabilityCheckerStateStore().read()
        return {
            "agents": [
                {
                    "name": "Product Discovery",
                    "key": "product_discovery",
                    "status": product_discovery.status,
                    "last_run": product_discovery.last_run,
                    "processed": product_discovery.products_discovered,
                    "success": product_discovery.products_discovered,
                    "failures": 0,
                    "endpoint": "/automation/product-discovery/run",
                },
                {
                    "name": "Price Monitor",
                    "key": "price_monitor",
                    "status": price_monitor.status,
                    "last_run": price_monitor.last_run,
                    "processed": price_monitor.products_checked,
                    "success": price_monitor.prices_updated,
                    "failures": 0,
                    "endpoint": "/automation/price-monitor/run",
                },
                {
                    "name": "Affiliate Manager",
                    "key": "affiliate_manager",
                    "status": affiliate_manager.status,
                    "last_run": affiliate_manager.last_run,
                    "processed": affiliate_manager.links_generated,
                    "success": affiliate_manager.links_generated,
                    "failures": 0,
                    "endpoint": "/automation/affiliate-manager/run",
                },
                {
                    "name": "Availability Checker",
                    "key": "availability_checker",
                    "status": availability_checker.status,
                    "last_run": availability_checker.last_run,
                    "processed": availability_checker.checked,
                    "success": availability_checker.updated,
                    "failures": 0,
                    "endpoint": "/automation/availability/run",
                },
            ]
        }

    def connectors(self) -> dict[str, Any]:
        manager = ConnectorManager()
        return {
            "connectors": [
                {
                    "provider": health.provider,
                    "status": health.status,
                    "message": health.message,
                    "product_count": len(manager.get_connector(health.provider).discover_products())
                    if manager.get_connector(health.provider)
                    else 0,
                }
                for health in manager.health_checks()
            ]
        }

    def products(self) -> dict[str, Any]:
        latest = self.db.scalar(select(Product).order_by(Product.created_at.desc(), Product.id.desc()).limit(1))
        identity_state = IdentityMappingService(self.db).health()
        return {
            "master_products": self._count(Product.id),
            "marketplace_sources": self._count(ProductSource.id),
            "products_added_today": 0,
            "duplicate_prevented": identity_state.duplicate_prevented,
            "latest_product": latest.title if latest else None,
        }

    def affiliate(self) -> dict[str, Any]:
        links = AffiliateLinkRepository(self.db).list_links()[:12]
        return {
            "generated_links": self._count(AffiliateLink.id),
            "updated_today": 0,
            "broken_links": self._count_where(AffiliateLink.id, AffiliateLink.status == "INVALID"),
            "providers": self._distinct_count(AffiliateLink.provider),
            "latest_links": [
                {
                    "id": link.id,
                    "provider": link.provider,
                    "status": link.status,
                    "affiliate_url": link.affiliate_url,
                    "product_source_id": link.product_source_id,
                }
                for link in links
            ],
        }

    def availability(self) -> dict[str, Any]:
        return {
            "in_stock": self._availability_count("IN_STOCK"),
            "out_of_stock": self._availability_count("OUT_OF_STOCK"),
            "limited": self._availability_count("LIMITED_STOCK"),
            "preorder": self._availability_count("PREORDER"),
            "unknown": self._availability_count("UNKNOWN"),
            "latest": [
                {
                    "id": row.id,
                    "provider": row.provider,
                    "status": row.status,
                    "quantity": row.quantity,
                    "product_source_id": row.product_source_id,
                }
                for row in AvailabilityRepository(self.db).list_statuses()[:12]
            ],
        }

    def recent_logs(self) -> list[dict[str, str]]:
        log_dir = Path(__file__).resolve().parents[1] / "automation" / "logs"
        rows: list[dict[str, str]] = []
        for path in sorted(log_dir.glob("*.log")):
            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()[-8:]
            except OSError:
                continue
            rows.extend({"source": path.name, "line": line} for line in lines)
        return rows[-40:]

    def _count(self, column: Any) -> int:
        return int(self.db.scalar(select(func.count(column))) or 0)

    def _count_where(self, column: Any, clause: Any) -> int:
        return int(self.db.scalar(select(func.count(column)).where(clause)) or 0)

    def _distinct_count(self, column: Any) -> int:
        return int(self.db.scalar(select(func.count(func.distinct(column)))) or 0)

    def _availability_count(self, status: str) -> int:
        return self._count_where(AvailabilityStatus.id, AvailabilityStatus.status == status)

    def _healthy_count(self, health_checks: list[Any]) -> str:
        healthy = sum(1 for item in health_checks if item.status == "ready")
        return f"{healthy}/{len(health_checks)}"

