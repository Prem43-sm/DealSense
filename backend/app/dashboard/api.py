from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dashboard.service import DashboardService
from app.database.connection import get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)) -> dict[str, object]:
    return DashboardService(db).summary()


@router.get("/automation")
def dashboard_automation(db: Session = Depends(get_db)) -> dict[str, object]:
    return DashboardService(db).automation()


@router.get("/connectors")
def dashboard_connectors(db: Session = Depends(get_db)) -> dict[str, object]:
    return DashboardService(db).connectors()


@router.get("/products")
def dashboard_products(db: Session = Depends(get_db)) -> dict[str, object]:
    return DashboardService(db).products()


@router.get("/affiliate")
def dashboard_affiliate(db: Session = Depends(get_db)) -> dict[str, object]:
    return DashboardService(db).affiliate()


@router.get("/availability")
def dashboard_availability(db: Session = Depends(get_db)) -> dict[str, object]:
    return DashboardService(db).availability()

