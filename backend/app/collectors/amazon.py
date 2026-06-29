from app.schemas.price import PriceObservation


def fetch_amazon_prices() -> list[PriceObservation]:
    return [
        PriceObservation(
            title="Lenovo LOQ",
            brand="Lenovo",
            category="Gaming Laptops",
            price=69999,
            availability=True,
            affiliate_url="https://amazon.example.com/lenovo-loq?tag=dealsense",
            store="Amazon",
            description="Lenovo LOQ gaming laptop with RTX graphics and high-refresh display.",
        ),
        PriceObservation(
            title="ASUS TUF Gaming",
            brand="ASUS",
            category="Gaming Laptops",
            price=74999,
            availability=True,
            affiliate_url="https://amazon.example.com/asus-tuf?tag=dealsense",
            store="Amazon",
            description="Durable ASUS TUF Gaming laptop for mainstream gaming.",
        ),
    ]
