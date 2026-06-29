from app.schemas.price import PriceObservation


def fetch_flipkart_prices() -> list[PriceObservation]:
    return [
        PriceObservation(
            title="Acer Nitro V",
            brand="Acer",
            category="Gaming Laptops",
            price=67999,
            availability=True,
            affiliate_url="https://flipkart.example.com/acer-nitro-v?affid=dealsense",
            store="Flipkart",
            description="Acer Nitro V gaming laptop with strong value pricing.",
        ),
        PriceObservation(
            title="HP Victus",
            brand="HP",
            category="Gaming Laptops",
            price=71999,
            availability=True,
            affiliate_url="https://flipkart.example.com/hp-victus?affid=dealsense",
            store="Flipkart",
            description="HP Victus laptop for gaming, students, and creators.",
        ),
    ]
