from decimal import Decimal

from app.connectors.base_connector import BaseConnector
from app.connectors.logger import get_connector_logger
from app.connectors.models import AffiliateLinkData, AvailabilityData, ConnectorHealth, PriceData, ProductData


MOCK_PRODUCTS = [
    ("Lenovo LOQ RTX 4050", "Lenovo", "Gaming Laptops", ["69999", "68999", "67999"]),
    ("HP Victus", "HP", "Gaming Laptops", ["71999", "70999", "70999"]),
    ("ASUS TUF", "ASUS", "Gaming Laptops", ["74999", "73999", "72999"]),
    ("Acer Nitro V", "Acer", "Gaming Laptops", ["67999", "66999", "66999"]),
    ("Samsung Galaxy S25", "Samsung", "Smartphones", ["109999", "108999", "106999"]),
    ("iPhone 17", "Apple", "Smartphones", ["129999", "127999", "127999"]),
    ("OnePlus 14", "OnePlus", "Smartphones", ["69999", "68999", "67999"]),
    ("Logitech MX Master", "Logitech", "Accessories", ["8999", "8499", "8499"]),
    ("Sony WH1000XM5", "Sony", "Audio", ["29999", "28999", "27999"]),
    ("Samsung 990 EVO SSD", "Samsung", "Storage", ["8999", "8799", "8499"]),
]


class BaseMockConnector(BaseConnector):
    provider_name = "mock"
    display_name = "Mock"
    external_prefix = "MOCK"
    price_offset = 0

    def __init__(self) -> None:
        self.logger = get_connector_logger(self.provider_name)

    def discover_products(self) -> list[ProductData]:
        self.logger.info("Mock product discovery", extra={"_provider": self.provider_name})
        return [
            ProductData(
                provider=self.provider_name,
                title=title,
                brand=brand,
                category=category,
                description=f"{title} discovered from {self.display_name} mock connector.",
                image_url=None,
                external_id=self._external_id(index),
                product_url=f"https://{self.provider_name}.example.com/products/{self._external_id(index)}",
                canonical_url=f"https://{self.provider_name}.example.com/products/{self._external_id(index)}",
            )
            for index, (title, brand, category, _prices) in enumerate(MOCK_PRODUCTS, start=1)
        ]

    def get_product(self, external_product_id: str) -> ProductData | None:
        return next(
            (product for product in self.discover_products() if product.external_id == external_product_id),
            None,
        )

    def get_prices(self, external_product_id: str) -> PriceData | None:
        product_index = self._index_from_external_id(external_product_id)
        if product_index is None:
            return None

        _title, _brand, _category, prices = MOCK_PRODUCTS[product_index - 1]
        price = Decimal(prices[min(self.price_offset, len(prices) - 1)])
        self.logger.info(
            "Mock price fetched",
            extra={"_provider": self.provider_name, "_external_id": external_product_id, "_price": price},
        )
        return PriceData(
            provider=self.provider_name,
            external_id=external_product_id,
            price=price,
            currency="INR",
        )

    def get_availability(self, external_product_id: str) -> AvailabilityData | None:
        if self._index_from_external_id(external_product_id) is None:
            return None
        return AvailabilityData(
            provider=self.provider_name,
            external_id=external_product_id,
            available=True,
            status="in_stock",
        )

    def generate_affiliate_url(self, product_url: str) -> AffiliateLinkData:
        return AffiliateLinkData(provider=self.provider_name, url=f"{product_url}?ref=dealsense")

    def health_check(self) -> ConnectorHealth:
        return ConnectorHealth(provider=self.provider_name, status="ready", message="Mock connector ready")

    def _external_id(self, index: int) -> str:
        return f"{self.external_prefix}-{index:04d}"

    def _index_from_external_id(self, external_product_id: str) -> int | None:
        prefix = f"{self.external_prefix}-"
        if not external_product_id.startswith(prefix):
            return None
        try:
            index = int(external_product_id.removeprefix(prefix))
        except ValueError:
            return None
        if index < 1 or index > len(MOCK_PRODUCTS):
            return None
        return index

