from typing import Any

from sqlalchemy.orm import Session

from app.analytics.events import (
    record_affiliate_click,
    record_compare,
    record_detail_visit,
    record_search,
    record_view,
    record_wishlist,
)
from app.analytics.repository import ProductAnalyticsRepository
from app.models.product_analytics import ProductAnalytics


class AnalyticsService:
    def __init__(self, db: Session, repository: ProductAnalyticsRepository | None = None) -> None:
        self.db = db
        self.repository = repository or ProductAnalyticsRepository(db)

    def record_view(self, product_id: int) -> dict[str, Any]:
        return self._event_response(record_view(self.repository, product_id))

    def record_search(self, query: str) -> dict[str, Any]:
        return {"status": "success", "matched_products": record_search(self.repository, query)}

    def record_affiliate_click(self, product_source_id: int) -> dict[str, Any]:
        row = record_affiliate_click(self.repository, product_source_id)
        if row is None:
            return {"status": "ignored", "reason": "product_source_not_found"}
        return self._event_response(row)

    def record_compare(self, product_id: int) -> dict[str, Any]:
        return self._event_response(record_compare(self.repository, product_id))

    def record_wishlist(self, product_id: int) -> dict[str, Any]:
        return self._event_response(record_wishlist(self.repository, product_id))

    def record_detail_visit(self, product_id: int) -> dict[str, Any]:
        return self._event_response(record_detail_visit(self.repository, product_id))

    def record_detail_visit_by_slug(self, slug: str) -> dict[str, Any]:
        product_id = self.repository.product_id_for_slug(slug)
        if product_id is None:
            return {"status": "ignored", "reason": "product_not_found"}
        return self.record_detail_visit(product_id)

    def trending(self, limit: int = 10) -> list[dict[str, Any]]:
        return [self._ranked_response(row) for row in self.repository.get_trending(limit)]

    def popular(self, limit: int = 10) -> list[dict[str, Any]]:
        return [self._ranked_response(row) for row in self.repository.get_popular(limit)]

    def top_clicked(self, limit: int = 10) -> list[dict[str, Any]]:
        return [self._ranked_response(row) for row in self.repository.get_top_clicked(limit)]

    def top_searches(self, limit: int = 10) -> list[dict[str, Any]]:
        return [self._ranked_response(row) for row in self.repository.get_top_searches(limit)]

    def dashboard(self) -> dict[str, Any]:
        totals = self.repository.dashboard_totals()
        trending = self.trending(10)
        popular = self.popular(10)
        clicked = self.top_clicked(10)
        top_product = trending[0]["title"] if trending else None
        clicks = totals["affiliate_clicks"]
        ctr = round((clicks / totals["views_today"]) * 100, 2) if totals["views_today"] else 0.0
        return {
            **totals,
            "ctr": ctr,
            "top_product": top_product,
            "top_products": trending,
            "top_searches": self.top_searches(10),
            "top_affiliate_clicks": clicked,
            "most_viewed": popular,
        }

    def recalculate_scores(self) -> dict[str, Any]:
        count = self.repository.recalculate_scores()
        return {"status": "success", "records_updated": count}

    def _event_response(self, row: ProductAnalytics) -> dict[str, Any]:
        return {"status": "success", "product_id": row.product_id, "date": row.date.isoformat(), "score": row.score}

    def _ranked_response(self, row: ProductAnalytics) -> dict[str, Any]:
        return {
            "product_id": row.product_id,
            "title": row.product.title if row.product else "Unknown product",
            "views": row.views,
            "searches": row.searches,
            "affiliate_clicks": row.affiliate_clicks,
            "wishlist_adds": row.wishlist_adds,
            "compare_adds": row.compare_adds,
            "detail_page_visits": row.detail_page_visits,
            "score": row.score,
        }
