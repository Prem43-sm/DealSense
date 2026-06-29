import logging
from pathlib import Path
from typing import Any


LOG_DIR = Path(__file__).resolve().parents[1] / "logs"


class AgentLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        extra: dict[str, Any] = {
            key.removeprefix("_"): value
            for key, value in record.__dict__.items()
            if key.startswith("_")
        }
        if not extra:
            return base
        details = " ".join(f"{key}={value}" for key, value in extra.items())
        return f"{base} {details}"


def get_agent_logger(agent_name: str, level: str = "INFO") -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(f"automation.{agent_name}")
    logger.setLevel(level.upper())
    logger.propagate = False

    log_path = LOG_DIR / f"{agent_name}.log"
    existing_paths = {
        getattr(handler, "baseFilename", None)
        for handler in logger.handlers
        if isinstance(handler, logging.FileHandler)
    }
    if str(log_path) not in existing_paths:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(AgentLogFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)

    return logger
