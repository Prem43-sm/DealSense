import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database.connection import get_db
from app.models.deal import Deal
from app.schemas.deal import DealRead

logger = logging.getLogger(__name__)
router = APIRouter(tags=["deals"])


@router.get("/deals", response_model=list[DealRead])
def list_deals(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[Deal]:
    offset = (page - 1) * limit
    logger.info("Listing deals", extra={"_page": page, "_limit": limit})
    return list(
        db.scalars(
            select(Deal)
            .options(joinedload(Deal.product))
            .order_by(Deal.deal_score.desc(), Deal.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    )
