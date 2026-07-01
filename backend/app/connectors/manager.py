from importlib import import_module
from inspect import isclass
from pkgutil import iter_modules

from app.connectors import providers
from app.connectors.base_connector import BaseConnector
from app.connectors.models import ConnectorHealth


class ConnectorManager:
    def __init__(self) -> None:
        self._connectors = self._discover_connectors()

    def list_providers(self) -> list[str]:
        return sorted(self._connectors)

    def get_connector(self, provider_name: str) -> BaseConnector | None:
        return self._connectors.get(provider_name.strip().lower())

    def health_checks(self) -> list[ConnectorHealth]:
        return [connector.health_check() for connector in self._connectors.values()]

    def health_check(self, provider_name: str) -> ConnectorHealth | None:
        connector = self.get_connector(provider_name)
        if connector is None:
            return None
        return connector.health_check()

    def all_connectors(self) -> list[BaseConnector]:
        return [self._connectors[name] for name in self.list_providers()]

    def _discover_connectors(self) -> dict[str, BaseConnector]:
        connectors: dict[str, BaseConnector] = {}
        for module_info in iter_modules(providers.__path__):
            if module_info.name.startswith("_") or module_info.name == "mock_base":
                continue
            module = import_module(f"{providers.__name__}.{module_info.name}.connector")
            for value in vars(module).values():
                if (
                    isclass(value)
                    and issubclass(value, BaseConnector)
                    and value is not BaseConnector
                    and value.__module__ == module.__name__
                ):
                    connector = value()
                    connectors[connector.provider_name] = connector
        return connectors
