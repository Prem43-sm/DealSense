import logging
from pathlib import Path


LOG_DIR = Path(__file__).resolve().parents[1] / "logs"


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
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)

    return logger

