import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.analytics.service import AnalyticsService
from app.collectors import fetch_amazon_prices, fetch_cuelinks_prices, fetch_flipkart_prices
from app.config import get_settings
from app.database.connection import SessionLocal
from app.schemas.price import PriceObservation
from app.services.price_service import process_observations

logger = logging.getLogger(__name__)


def collect_all_prices() -> list[PriceObservation]:
    observations: list[PriceObservation] = []
    collectors = [
        ("amazon", fetch_amazon_prices),
        ("flipkart", fetch_flipkart_prices),
        ("cuelinks", fetch_cuelinks_prices),
    ]

    for name, collector in collectors:
        try:
            collector_results = collector()
            observations.extend(collector_results)
            logger.info(
                "Collector completed",
                extra={"_collector": name, "_count": len(collector_results)},
            )
        except Exception:
            logger.exception("Collector failed", extra={"_collector": name})

    return observations


def run_price_refresh() -> int:
    observations = collect_all_prices()
    if not observations:
        logger.warning("Price refresh skipped because collectors returned no observations")
        return 0

    db = SessionLocal()
    try:
        count = process_observations(db, observations)
        logger.info("Price refresh completed", extra={"_count": count})
        return count
    except Exception:
        db.rollback()
        logger.exception("Price refresh failed")
        raise
    finally:
        db.close()


def run_analytics_score_recalculation() -> int:
    db = SessionLocal()
    try:
        result = AnalyticsService(db).recalculate_scores()
        records_updated = int(result["records_updated"])
        logger.info("Analytics score recalculation completed", extra={"_records_updated": records_updated})
        return records_updated
    except Exception:
        db.rollback()
        logger.exception("Analytics score recalculation failed")
        raise
    finally:
        db.close()


def create_scheduler() -> BackgroundScheduler:
    settings = get_settings()
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(
        run_price_refresh,
        trigger=IntervalTrigger(hours=settings.price_refresh_hours),
        id="price_refresh",
        name="Refresh product prices and deals",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    return scheduler
