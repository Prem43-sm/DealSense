from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.automation.agents.availability_checker.repository import AvailabilityRepository
from app.database.connection import get_db

router = APIRouter(prefix="/availability", tags=["availability"])


class AvailabilityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_source_id: int
    provider: str
    status: str
    quantity: int | None = None
    last_checked: datetime
    last_changed: datetime
    created_at: datetime
    updated_at: datetime


@router.get("", response_model=list[AvailabilityRead])
def list_availability(db: Session = Depends(get_db)) -> list[object]:
    return AvailabilityRepository(db).list_statuses()


@router.get("/{product_source_id}", response_model=list[AvailabilityRead])
def list_availability_for_source(
    product_source_id: int,
    db: Session = Depends(get_db),
) -> list[object]:
    return AvailabilityRepository(db).list_statuses_for_source(product_source_id)
