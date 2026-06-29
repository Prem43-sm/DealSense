from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from app.models.deal import Deal


def calculate_discount_percent(old_price: Decimal, new_price: Decimal) -> Decimal:
    if old_price <= 0 or new_price >= old_price:
        return Decimal("0.00")
    discount = ((old_price - new_price) / old_price) * Decimal("100")
    return discount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_deal_score(discount_percent: Decimal) -> int:
    return min(int(discount_percent * Decimal("5")), 100)


def create_deal_if_discounted(
    db: Session,
    *,
    product_id: int,
    old_price: Decimal,
    new_price: Decimal,
) -> Deal | None:
    discount_percent = calculate_discount_percent(old_price, new_price)
    deal_score = calculate_deal_score(discount_percent)

    if deal_score <= 0:
        return None

    deal = Deal(
        product_id=product_id,
        discount_percent=discount_percent,
        deal_score=deal_score,
    )
    db.add(deal)
    db.flush()
    return deal
