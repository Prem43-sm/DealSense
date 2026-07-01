from enum import StrEnum


class AvailabilityState(StrEnum):
    IN_STOCK = "IN_STOCK"
    LIMITED_STOCK = "LIMITED_STOCK"
    PREORDER = "PREORDER"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    DISCONTINUED = "DISCONTINUED"
    UNKNOWN = "UNKNOWN"


ALIASES = {
    "in stock": AvailabilityState.IN_STOCK,
    "instock": AvailabilityState.IN_STOCK,
    "available": AvailabilityState.IN_STOCK,
    "limited stock": AvailabilityState.LIMITED_STOCK,
    "low stock": AvailabilityState.LIMITED_STOCK,
    "preorder": AvailabilityState.PREORDER,
    "pre-order": AvailabilityState.PREORDER,
    "out of stock": AvailabilityState.OUT_OF_STOCK,
    "sold out": AvailabilityState.OUT_OF_STOCK,
    "discontinued": AvailabilityState.DISCONTINUED,
    "unknown": AvailabilityState.UNKNOWN,
}


def normalize_status(status: str | None) -> AvailabilityState | None:
    if status is None:
        return None
    normalized = status.strip().replace("_", " ").upper()
    for state in AvailabilityState:
        if normalized == state.value.replace("_", " "):
            return state
    return ALIASES.get(status.strip().replace("_", " ").lower())

