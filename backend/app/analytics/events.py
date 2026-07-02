import logging
from pathlib import Path

from app.analytics.repository import ProductAnalyticsRepository
from app.models.product_analytics import ProductAnalytics


def get_analytics_logger() -> logging.Logger:
    logger = logging.getLogger("app.analytics")
    if logger.handlers:
        return logger

    log_dir = Path(__file__).resolve().parents[1] / "automation" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_dir / "analytics.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = True
    return logger


def record_view(repository: ProductAnalyticsRepository, product_id: int) -> ProductAnalytics:
    row = repository.increment_views(product_id)
    get_analytics_logger().info("Event view product=%s", product_id)
    return row


def record_search(repository: ProductAnalyticsRepository, query: str) -> int:
    product_ids = repository.product_ids_for_search(query)
    for product_id in product_ids:
        repository.increment_searches(product_id)
    get_analytics_logger().info("Event search query=%s matched=%s", query, len(product_ids))
    return len(product_ids)


def record_affiliate_click(repository: ProductAnalyticsRepository, product_source_id: int) -> ProductAnalytics | None:
    row = repository.increment_clicks(product_source_id)
    get_analytics_logger().info("Event affiliate_click product_source=%s", product_source_id)
    return row


def record_compare(repository: ProductAnalyticsRepository, product_id: int) -> ProductAnalytics:
    row = repository.increment_compare(product_id)
    get_analytics_logger().info("Event compare product=%s", product_id)
    return row


def record_wishlist(repository: ProductAnalyticsRepository, product_id: int) -> ProductAnalytics:
    row = repository.increment_wishlist(product_id)
    get_analytics_logger().info("Event wishlist product=%s", product_id)
    return row


def record_detail_visit(repository: ProductAnalyticsRepository, product_id: int) -> ProductAnalytics:
    row = repository.increment_detail_visit(product_id)
    get_analytics_logger().info("Event detail_visit product=%s", product_id)
    return row
