from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.analytics.service import AnalyticsService
from app.database.connection import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])


class ProductEvent(BaseModel):
    product_id: int = Field(gt=0)


class SearchEvent(BaseModel):
    query: str = Field(min_length=1, max_length=255)


class AffiliateClickEvent(BaseModel):
    product_source_id: int = Field(gt=0)


class DetailVisitBySlugEvent(BaseModel):
    slug: str = Field(min_length=1, max_length=255)


@router.get("/trending")
def trending(limit: int = Query(default=10, ge=1, le=50), db: Session = Depends(get_db)) -> list[dict[str, object]]:
    return AnalyticsService(db).trending(limit)


@router.get("/popular")
def popular(limit: int = Query(default=10, ge=1, le=50), db: Session = Depends(get_db)) -> list[dict[str, object]]:
    return AnalyticsService(db).popular(limit)


@router.get("/top-clicked")
def top_clicked(limit: int = Query(default=10, ge=1, le=50), db: Session = Depends(get_db)) -> list[dict[str, object]]:
    return AnalyticsService(db).top_clicked(limit)


@router.get("/top-searches")
def top_searches(limit: int = Query(default=10, ge=1, le=50), db: Session = Depends(get_db)) -> list[dict[str, object]]:
    return AnalyticsService(db).top_searches(limit)


@router.get("/dashboard")
def analytics_dashboard(db: Session = Depends(get_db)) -> dict[str, object]:
    return AnalyticsService(db).dashboard()


@router.post("/events/view")
def track_view(event: ProductEvent, db: Session = Depends(get_db)) -> dict[str, object]:
    return AnalyticsService(db).record_view(event.product_id)


@router.post("/events/search")
def track_search(event: SearchEvent, db: Session = Depends(get_db)) -> dict[str, object]:
    return AnalyticsService(db).record_search(event.query)


@router.post("/events/affiliate-click")
def track_affiliate_click(event: AffiliateClickEvent, db: Session = Depends(get_db)) -> dict[str, object]:
    return AnalyticsService(db).record_affiliate_click(event.product_source_id)


@router.post("/events/compare")
def track_compare(event: ProductEvent, db: Session = Depends(get_db)) -> dict[str, object]:
    return AnalyticsService(db).record_compare(event.product_id)


@router.post("/events/wishlist")
def track_wishlist(event: ProductEvent, db: Session = Depends(get_db)) -> dict[str, object]:
    return AnalyticsService(db).record_wishlist(event.product_id)


@router.post("/events/detail-visit")
def track_detail_visit(event: ProductEvent, db: Session = Depends(get_db)) -> dict[str, object]:
    return AnalyticsService(db).record_detail_visit(event.product_id)


@router.post("/events/detail-visit-by-slug")
def track_detail_visit_by_slug(event: DetailVisitBySlugEvent, db: Session = Depends(get_db)) -> dict[str, object]:
    return AnalyticsService(db).record_detail_visit_by_slug(event.slug)
