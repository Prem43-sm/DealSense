import logging
from pathlib import Path
from typing import Any


class IdentityLogFormatter(logging.Formatter):
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


def get_identity_logger() -> logging.Logger:
    log_dir = Path(__file__).resolve().parents[1] / "automation" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "identity.log"

    logger = logging.getLogger("identity")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    existing_paths = {
        getattr(handler, "baseFilename", None)
        for handler in logger.handlers
        if isinstance(handler, logging.FileHandler)
    }
    if str(log_path) not in existing_paths:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(IdentityLogFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)

    return logger

