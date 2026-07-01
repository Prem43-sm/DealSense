from decimal import Decimal, ROUND_HALF_UP

from pydantic import BaseModel


class PriceComparison(BaseModel):
    price_changed: bool
    old_price: Decimal | None
    new_price: Decimal
    difference: Decimal
    percentage_change: Decimal


def compare_price(existing_price: Decimal | None, new_price: Decimal) -> PriceComparison:
    if existing_price is None:
        return PriceComparison(
            price_changed=True,
            old_price=None,
            new_price=new_price,
            difference=Decimal("0.00"),
            percentage_change=Decimal("0.00"),
        )

    old_price = Decimal(existing_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    difference = (new_price - old_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    percentage_change = Decimal("0.00")
    if old_price > 0 and difference != 0:
        percentage_change = ((difference / old_price) * Decimal("100")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    return PriceComparison(
        price_changed=old_price != new_price,
        old_price=old_price,
        new_price=new_price,
        difference=difference,
        percentage_change=percentage_change,
    )

