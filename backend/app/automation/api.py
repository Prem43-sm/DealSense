from fastapi import APIRouter, Depends

from app.automation.services.health_service import HealthService, get_health_service

router = APIRouter(prefix="/automation", tags=["automation"])


@router.get("/status")
def automation_status(
    health_service: HealthService = Depends(get_health_service),
) -> dict[str, object]:
    return health_service.status()

