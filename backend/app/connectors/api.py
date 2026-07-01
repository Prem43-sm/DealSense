from fastapi import APIRouter, HTTPException

from app.connectors.manager import ConnectorManager

router = APIRouter(prefix="/connectors", tags=["connectors"])


@router.get("")
def list_connectors() -> dict[str, object]:
    manager = ConnectorManager()
    return {
        "providers": manager.list_providers(),
        "connectors": [health.model_dump() for health in manager.health_checks()],
    }


@router.get("/{provider}/health")
def connector_health(provider: str) -> dict[str, object]:
    health = ConnectorManager().health_check(provider)
    if health is None:
        raise HTTPException(status_code=404, detail="Connector not found")
    return health.model_dump()

