from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict


class SourceProduct(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None
    brand: str | None
    category: str | None
    description: str | None = None
    image_url: str | None = None
    external_id: str | None = None
    store: str | None = None
    url: str | None = None


class ProductSource(ABC):
    name: str

    @abstractmethod
    def fetch_products(self) -> list[SourceProduct]:
        raise NotImplementedError


class MockSource(ProductSource):
    name = "Mock Source"

    def fetch_products(self) -> list[SourceProduct]:
        products = [
            ("Lenovo LOQ RTX 4050", "Lenovo", "Gaming Laptops"),
            ("HP Victus", "HP", "Gaming Laptops"),
            ("ASUS TUF", "ASUS", "Gaming Laptops"),
            ("Acer Nitro V", "Acer", "Gaming Laptops"),
            ("Samsung Galaxy S25", "Samsung", "Smartphones"),
            ("iPhone 17", "Apple", "Smartphones"),
            ("OnePlus 14", "OnePlus", "Smartphones"),
            ("Logitech MX Master", "Logitech", "Accessories"),
            ("Sony WH1000XM5", "Sony", "Audio"),
            ("Samsung 990 EVO SSD", "Samsung", "Storage"),
        ]
        return [
            SourceProduct(
                title=title,
                brand=brand,
                category=category,
                description=f"{title} discovered from the mock product source.",
                image_url=None,
                external_id=f"mock-{index}",
                store=self.name,
                url=f"https://example.com/products/mock-{index}",
            )
            for index, (title, brand, category) in enumerate(products, start=1)
        ]


def get_product_sources() -> list[ProductSource]:
    return [MockSource()]

