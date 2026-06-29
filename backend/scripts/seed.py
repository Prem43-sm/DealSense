import logging
import sys
from pathlib import Path

from sqlalchemy import select

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.collectors import fetch_amazon_prices, fetch_cuelinks_prices, fetch_flipkart_prices
from app.database.connection import SessionLocal
from app.logging_config import configure_logging
from app.models.product import Product
from app.models.store import Store
from app.schemas.price import PriceObservation
from app.services.price_service import process_observations, slugify

configure_logging()
logger = logging.getLogger(__name__)


PRODUCTS = [
    {
        "title": "Lenovo LOQ",
        "brand": "Lenovo",
        "category": "Gaming Laptops",
        "description": "Lenovo LOQ gaming laptop with RTX graphics and high-refresh display.",
    },
    {
        "title": "ASUS TUF Gaming",
        "brand": "ASUS",
        "category": "Gaming Laptops",
        "description": "Durable ASUS TUF Gaming laptop for mainstream gaming.",
    },
    {
        "title": "Acer Nitro V",
        "brand": "Acer",
        "category": "Gaming Laptops",
        "description": "Acer Nitro V gaming laptop with strong value pricing.",
    },
    {
        "title": "HP Victus",
        "brand": "HP",
        "category": "Gaming Laptops",
        "description": "HP Victus laptop for gaming, students, and creators.",
    },
    {
        "title": "Dell G15",
        "brand": "Dell",
        "category": "Gaming Laptops",
        "description": "Dell G15 performance gaming laptop with reliable thermals.",
    },
]

STORES = [
    {"name": "Amazon", "logo_url": None},
    {"name": "Flipkart", "logo_url": None},
    {"name": "Croma", "logo_url": None},
]


def seed_products_and_stores() -> None:
    db = SessionLocal()
    try:
        for store_data in STORES:
            store = db.scalar(select(Store).where(Store.name == store_data["name"]))
            if store is None:
                db.add(Store(**store_data))
                logger.info("Seeded store", extra={"_store": store_data["name"]})

        for product_data in PRODUCTS:
            slug = slugify(f"{product_data['brand']} {product_data['title']}")
            product = db.scalar(select(Product).where(Product.slug == slug))
            if product is None:
                db.add(Product(slug=slug, **product_data))
                logger.info("Seeded product", extra={"_product": slug})

        db.commit()
    except Exception:
        db.rollback()
        logger.exception("Seed failed")
        raise
    finally:
        db.close()


def seed_mock_prices() -> None:
    observations: list[PriceObservation] = [
        *fetch_amazon_prices(),
        *fetch_flipkart_prices(),
        *fetch_cuelinks_prices(),
    ]
    db = SessionLocal()
    try:
        count = process_observations(db, observations)
        logger.info("Seeded mock prices", extra={"_count": count})
    except Exception:
        db.rollback()
        logger.exception("Mock price seed failed")
        raise
    finally:
        db.close()


def main() -> None:
    seed_products_and_stores()
    seed_mock_prices()
    logger.info("Seed completed")


if __name__ == "__main__":
    main()
