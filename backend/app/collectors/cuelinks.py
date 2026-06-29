from app.schemas.price import PriceObservation


def fetch_cuelinks_prices() -> list[PriceObservation]:
    return [
        PriceObservation(
            title="Dell G15",
            brand="Dell",
            category="Gaming Laptops",
            price=78999,
            availability=True,
            affiliate_url="https://croma.example.com/dell-g15?utm_source=dealsense",
            store="Croma",
            description="Dell G15 performance gaming laptop with reliable thermals.",
        ),
        PriceObservation(
            title="Lenovo LOQ",
            brand="Lenovo",
            category="Gaming Laptops",
            price=71999,
            availability=True,
            affiliate_url="https://croma.example.com/lenovo-loq?utm_source=dealsense",
            store="Croma",
            description="Lenovo LOQ gaming laptop available through Croma.",
        ),
    ]
