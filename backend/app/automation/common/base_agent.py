import logging
from dataclasses import dataclass
from typing import Any, Protocol

from sqlalchemy.orm import Session


class AgentScheduler(Protocol):
    def register_agent(self, agent: "BaseAgent") -> None:
        ...


@dataclass(frozen=True)
class AgentRuntime:
    db: Session | None
    logger: logging.Logger
    config: Any
    scheduler: AgentScheduler | None
    services: dict[str, Any]


class BaseAgent:
    name = "base_agent"

    def __init__(self, runtime: AgentRuntime) -> None:
        self.runtime = runtime
        self._status = "ready"

    def start(self) -> None:
        self._status = "running"
        self.log("Agent started")

    def stop(self) -> None:
        self._status = "stopped"
        self.log("Agent stopped")

    def run(self) -> None:
        raise NotImplementedError("Agents must override run().")

    def health(self) -> dict[str, str]:
        return {"name": self.name, "status": self._status}

    def status(self) -> str:
        return self._status

    def log(self, message: str, **extra: Any) -> None:
        self.runtime.logger.info(message, extra={f"_{key}": value for key, value in extra.items()})

