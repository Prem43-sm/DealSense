import json
from abc import ABC, abstractmethod
from decimal import Decimal
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from app.models.product import Product


class SourcePrice(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    product_id: int
    store: str
    price: Decimal
    currency: str = "INR"


class PriceSource(ABC):
    name: str

    @abstractmethod
    def start_run(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def finish_run(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def fetch_price(self, product: Product) -> SourcePrice | None:
        raise NotImplementedError


class MockPriceSourceState:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path(__file__).resolve().parents[2] / "logs" / "price_monitor_mock_state.json"

    def read_run_count(self) -> int:
        if not self.path.exists():
            return 0
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return int(payload.get("run_count", 0))

    def write_run_count(self, run_count: int) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({"run_count": run_count}, indent=2), encoding="utf-8")


class MockPriceSource(PriceSource):
    name = "Mock Price Source"
    store = "Amazon"

    def __init__(self, state: MockPriceSourceState | None = None) -> None:
        self.state = state or MockPriceSourceState()
        self.run_count = self.state.read_run_count()

    def start_run(self) -> None:
        self.run_count = self.state.read_run_count() + 1

    def finish_run(self) -> None:
        self.state.write_run_count(self.run_count)

    def fetch_price(self, product: Product) -> SourcePrice | None:
        price = self._price_for_product(product)
        if price is None:
            return None
        return SourcePrice(product_id=product.id, store=self.store, price=price)

    def _price_for_product(self, product: Product) -> Decimal | None:
        key = f"{product.title} {product.slug}".lower()
        slug = product.slug.lower()
        sequence = self._sequence_for_key(key)
        if sequence is None:
            sequence = self._sequence_for_slug(slug)
        if sequence is None:
            return None
        index = min(max(self.run_count - 1, 0), len(sequence) - 1)
        return Decimal(sequence[index])

    def _sequence_for_slug(self, slug: str) -> list[str] | None:
        exact_matches = {
            "lenovo-loq-rtx-4050": ["69999", "68999", "68999", "67999"],
            "hp-hp-victus": ["71999", "71999", "70999", "70999"],
            "hp-victus": ["71999", "71999", "70999", "70999"],
            "asus-tuf": ["74999", "73999", "73999", "72999"],
            "acer-acer-nitro-v": ["67999", "67999", "66999", "66999"],
            "acer-nitro-v": ["67999", "67999", "66999", "66999"],
            "samsung-galaxy-s25": ["109999", "108999", "108999", "106999"],
            "iphone-17": ["129999", "129999", "127999", "127999"],
            "oneplus-14": ["69999", "68999", "68999", "67999"],
            "logitech-mx-master": ["8999", "8999", "8499", "8499"],
            "sony-wh1000xm5": ["29999", "28999", "28999", "27999"],
            "samsung-990-evo-ssd": ["8999", "8799", "8799", "8499"],
        }
        return exact_matches.get(slug)

    def _sequence_for_key(self, key: str) -> list[str] | None:
        if "hp victus" in key:
            return ["71999", "71999", "70999", "70999"]
        if "acer nitro" in key:
            return ["67999", "67999", "66999", "66999"]
        if "samsung galaxy s25" in key:
            return ["109999", "108999", "108999", "106999"]
        if "iphone 17" in key:
            return ["129999", "129999", "127999", "127999"]
        if "oneplus 14" in key:
            return ["69999", "68999", "68999", "67999"]
        if "logitech mx master" in key:
            return ["8999", "8999", "8499", "8499"]
        if "sony wh1000xm5" in key or "sony wh-1000xm5" in key:
            return ["29999", "28999", "28999", "27999"]
        if "samsung 990 evo" in key:
            return ["8999", "8799", "8799", "8499"]
        return None


def get_price_sources() -> list[PriceSource]:
    return [MockPriceSource()]
