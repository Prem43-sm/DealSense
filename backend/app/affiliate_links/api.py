from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.automation.agents.affiliate_manager.repository import AffiliateLinkRepository
from app.database.connection import get_db

router = APIRouter(prefix="/affiliate-links", tags=["affiliate-links"])


class AffiliateLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_source_id: int
    provider: str
    affiliate_url: str
    short_url: str | None = None
    tracking_id: str | None = None
    status: str
    last_generated: datetime
    last_checked: datetime | None = None
    last_valid: datetime | None = None
    click_count: int


@router.get("", response_model=list[AffiliateLinkRead])
def list_affiliate_links(db: Session = Depends(get_db)) -> list[object]:
    return AffiliateLinkRepository(db).list_links()


@router.get("/{product_source_id}", response_model=list[AffiliateLinkRead])
def list_affiliate_links_for_source(
    product_source_id: int,
    db: Session = Depends(get_db),
) -> list[object]:
    return AffiliateLinkRepository(db).list_links_for_source(product_source_id)
