from app.models.product_analytics import ProductAnalytics


def calculate_score(analytics: ProductAnalytics) -> int:
    return (
        analytics.views * 1
        + analytics.detail_page_visits * 2
        + analytics.affiliate_clicks * 5
        + analytics.wishlist_adds * 4
        + analytics.compare_adds * 3
        + analytics.searches * 2
    )
