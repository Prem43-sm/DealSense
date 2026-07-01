import logging
from pathlib import Path
from typing import Any


class ConnectorLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        extra: dict[str, Any] = {
            key.removeprefix("_"): value
            for key, value in record.__dict__.items()
            if key.startswith("_")
        }
        if not extra:
            return base
        return f"{base} " + " ".join(f"{key}={value}" for key, value in extra.items())


def get_connector_logger(provider_name: str) -> logging.Logger:
    log_dir = Path(__file__).resolve().parents[1] / "automation" / "logs" / "connectors"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{provider_name}.log"

    logger = logging.getLogger(f"connectors.{provider_name}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    existing_paths = {
        getattr(handler, "baseFilename", None)
        for handler in logger.handlers
        if isinstance(handler, logging.FileHandler)
    }
    if str(log_path) not in existing_paths:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(ConnectorLogFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)

    return logger

