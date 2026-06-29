import logging
import re
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.price import Price
from app.models.price_history import PriceHistory
from app.models.product import Product
from app.models.store import Store
from app.schemas.price import PriceObservation
from app.services.deal_service import create_deal_if_discounted

logger = logging.getLogger(__name__)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "product"


def get_or_create_store(db: Session, *, name: str, logo_url: str | None = None) -> Store:
    store = db.scalar(select(Store).where(Store.name == name))
    if store:
        if logo_url and store.logo_url != logo_url:
            store.logo_url = logo_url
        return store

    store = Store(name=name, logo_url=logo_url)
    db.add(store)
    db.flush()
    return store


def get_or_create_product(db: Session, observation: PriceObservation) -> Product:
    slug = slugify(f"{observation.brand or ''} {observation.title}")
    product = db.scalar(select(Product).where(Product.slug == slug))
    if product:
        return product

    product = Product(
        title=observation.title,
        slug=slug,
        brand=observation.brand,
        category=observation.category,
        image_url=observation.image_url,
        description=observation.description,
    )
    db.add(product)
    db.flush()
    return product


def record_price_observation(db: Session, observation: PriceObservation) -> Price:
    product = get_or_create_product(db, observation)
    store = get_or_create_store(db, name=observation.store, logo_url=observation.store_logo_url)
    new_price = Decimal(observation.price).quantize(Decimal("0.01"))

    current = db.scalar(
        select(Price).where(
            Price.product_id == product.id,
            Price.store_id == store.id,
        )
    )

    if current is None:
        current = Price(
            product_id=product.id,
            store_id=store.id,
            current_price=new_price,
            availability=observation.availability,
            affiliate_url=str(observation.affiliate_url),
        )
        db.add(current)
        db.add(PriceHistory(product_id=product.id, store_id=store.id, price=new_price))
        db.flush()
        logger.info("Created price for product=%s store=%s price=%s", product.slug, store.name, new_price)
        return current

    old_price = Decimal(current.current_price)
    price_changed = old_price != new_price
    availability_changed = current.availability != observation.availability

    if price_changed:
        current.current_price = new_price
        db.add(PriceHistory(product_id=product.id, store_id=store.id, price=old_price))
        create_deal_if_discounted(db, product_id=product.id, old_price=old_price, new_price=new_price)
        logger.info(
            "Updated price for product=%s store=%s old=%s new=%s",
            product.slug,
            store.name,
            old_price,
            new_price,
        )

    if availability_changed:
        current.availability = observation.availability
        logger.info("Updated availability for product=%s store=%s", product.slug, store.name)

    current.affiliate_url = str(observation.affiliate_url)
    db.flush()
    return current


def process_observations(db: Session, observations: list[PriceObservation]) -> int:
    count = 0
    for observation in observations:
        record_price_observation(db, observation)
        count += 1
    db.commit()
    return count
