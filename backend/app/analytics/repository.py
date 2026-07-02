from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import desc, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.analytics.scoring import calculate_score
from app.models.affiliate_link import AffiliateLink
from app.models.product import Product
from app.models.product_analytics import ProductAnalytics
from app.models.product_source import ProductSource


class ProductAnalyticsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def today(self) -> date:
        return datetime.now(UTC).date()

    def get_or_create(self, product_id: int, record_date: date | None = None) -> ProductAnalytics:
        analytics_date = record_date or self.today()
        analytics = self.db.scalar(
            select(ProductAnalytics).where(
                ProductAnalytics.product_id == product_id,
                ProductAnalytics.date == analytics_date,
            )
        )
        if analytics:
            return analytics

        analytics = ProductAnalytics(product_id=product_id, date=analytics_date)
        self.db.add(analytics)
        self.db.flush()
        return analytics

    def increment(self, product_id: int, field: str, amount: int = 1) -> ProductAnalytics:
        analytics = self.get_or_create(product_id)
        current = int(getattr(analytics, field))
        setattr(analytics, field, current + amount)
        analytics.score = calculate_score(analytics)
        self.db.commit()
        self.db.refresh(analytics)
        return analytics

    def increment_views(self, product_id: int) -> ProductAnalytics:
        return self.increment(product_id, "views")

    def increment_searches(self, product_id: int) -> ProductAnalytics:
        return self.increment(product_id, "searches")

    def increment_clicks(self, product_source_id: int) -> ProductAnalytics | None:
        product_source = self.db.get(ProductSource, product_source_id)
        if product_source is None:
            return None

        link = self.db.scalar(
            select(AffiliateLink).where(AffiliateLink.product_source_id == product_source_id).order_by(AffiliateLink.id)
        )
        if link:
            link.click_count += 1

        return self.increment(product_source.product_id, "affiliate_clicks")

    def increment_compare(self, product_id: int) -> ProductAnalytics:
        return self.increment(product_id, "compare_adds")

    def increment_wishlist(self, product_id: int) -> ProductAnalytics:
        return self.increment(product_id, "wishlist_adds")

    def increment_detail_visit(self, product_id: int) -> ProductAnalytics:
        return self.increment(product_id, "detail_page_visits")

    def product_id_for_slug(self, slug: str) -> int | None:
        return self.db.scalar(select(Product.id).where(Product.slug == slug))

    def product_ids_for_search(self, query: str, limit: int = 10) -> list[int]:
        normalized = f"%{query.strip().lower()}%"
        if normalized == "%%":
            return []
        return list(
            self.db.scalars(
                select(Product.id)
                .where(
                    or_(
                        func.lower(Product.title).like(normalized),
                        func.lower(Product.brand).like(normalized),
                        func.lower(Product.category).like(normalized),
                    )
                )
                .order_by(Product.created_at.desc(), Product.id.desc())
                .limit(limit)
            )
        )

    def recalculate_scores(self, record_date: date | None = None) -> int:
        statement = select(ProductAnalytics)
        if record_date is not None:
            statement = statement.where(ProductAnalytics.date == record_date)
        rows = list(self.db.scalars(statement))
        for row in rows:
            row.score = calculate_score(row)
        self.db.commit()
        return len(rows)

    def get_trending(self, limit: int = 10) -> list[ProductAnalytics]:
        return self._ranked(ProductAnalytics.score, limit)

    def get_popular(self, limit: int = 10) -> list[ProductAnalytics]:
        return self._ranked(ProductAnalytics.views, limit)

    def get_top_clicked(self, limit: int = 10) -> list[ProductAnalytics]:
        return self._ranked(ProductAnalytics.affiliate_clicks, limit)

    def get_top_searches(self, limit: int = 10) -> list[ProductAnalytics]:
        return self._ranked(ProductAnalytics.searches, limit)

    def dashboard_totals(self) -> dict[str, int]:
        today = self.today()
        row = self.db.execute(
            select(
                func.coalesce(func.sum(ProductAnalytics.views), 0),
                func.coalesce(func.sum(ProductAnalytics.searches), 0),
                func.coalesce(func.sum(ProductAnalytics.affiliate_clicks), 0),
                func.coalesce(func.sum(ProductAnalytics.wishlist_adds), 0),
            ).where(ProductAnalytics.date == today)
        ).one()
        return {
            "views_today": int(row[0] or 0),
            "searches_today": int(row[1] or 0),
            "affiliate_clicks": int(row[2] or 0),
            "wishlist_adds": int(row[3] or 0),
        }

    def _ranked(self, column: Any, limit: int) -> list[ProductAnalytics]:
        return list(
            self.db.scalars(
                select(ProductAnalytics)
                .options(selectinload(ProductAnalytics.product))
                .where(ProductAnalytics.date == self.today(), column > 0)
                .order_by(desc(column), ProductAnalytics.id.asc())
                .limit(limit)
            )
        )
