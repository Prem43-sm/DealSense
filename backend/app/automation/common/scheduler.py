from dataclasses import dataclass
from datetime import timedelta
from importlib import import_module
from inspect import isclass
from pkgutil import iter_modules
from typing import TypeAlias

from sqlalchemy.orm import Session

from app.automation import agents
from app.automation.common.base_agent import AgentRuntime, BaseAgent
from app.automation.common.logger import get_agent_logger
from app.automation.services.database_service import DatabaseService
from app.automation.services.notification_service import NotificationService
from app.automation.services.queue_service import QueueService

AgentClass: TypeAlias = type[BaseAgent]


@dataclass(frozen=True)
class ScheduleOption:
    name: str
    interval: timedelta


SUPPORTED_INTERVALS = {
    "30_minutes": ScheduleOption("30 minutes", timedelta(minutes=30)),
    "1_hour": ScheduleOption("1 hour", timedelta(hours=1)),
    "6_hours": ScheduleOption("6 hours", timedelta(hours=6)),
    "12_hours": ScheduleOption("12 hours", timedelta(hours=12)),
    "daily": ScheduleOption("Daily", timedelta(days=1)),
    "weekly": ScheduleOption("Weekly", timedelta(weeks=1)),
}


AGENT_ORDER = (
    "product_discovery",
    "price_monitor",
    "affiliate_manager",
    "availability_checker",
    "shopping_assistant",
    "content_generator",
)


class AutomationScheduler:
    def __init__(
        self,
        db: Session | None = None,
        database_service: DatabaseService | None = None,
        queue_service: QueueService | None = None,
        notification_service: NotificationService | None = None,
    ) -> None:
        self.db = db
        self.database_service = database_service or DatabaseService()
        self.queue_service = queue_service or QueueService()
        self.notification_service = notification_service or NotificationService()
        self.agents: list[BaseAgent] = []
        self.state = "idle"

    def discover_agent_classes(self) -> list[AgentClass]:
        discovered: list[AgentClass] = []
        for module_info in iter_modules(agents.__path__):
            if module_info.name.startswith("_"):
                continue
            module = import_module(f"{agents.__name__}.{module_info.name}.agent")
            for value in vars(module).values():
                if isclass(value) and issubclass(value, BaseAgent) and value is not BaseAgent:
                    discovered.append(value)

        return sorted(
            discovered,
            key=lambda agent_class: AGENT_ORDER.index(agent_class.name)
            if agent_class.name in AGENT_ORDER
            else len(AGENT_ORDER),
        )

    def register_all_agents(self) -> list[BaseAgent]:
        self.agents = []
        for agent_class in self.discover_agent_classes():
            config = agent_class.config_factory()
            logger = get_agent_logger(agent_class.name, config.LOG_LEVEL)
            runtime = AgentRuntime(
                db=self.db,
                logger=logger,
                config=config,
                scheduler=self,
                services={
                    "database": self.database_service,
                    "queue": self.queue_service,
                    "notification": self.notification_service,
                },
            )
            self.register_agent(agent_class(runtime))
        return self.agents

    def register_agent(self, agent: BaseAgent) -> None:
        self.agents.append(agent)

    def schedule_registered_agents(self) -> None:
        # Intentionally empty for Phase 2.1. Jobs are registered in a later phase.
        return None

    def status(self) -> str:
        return self.state

    def supported_intervals(self) -> list[str]:
        return list(SUPPORTED_INTERVALS.keys())
