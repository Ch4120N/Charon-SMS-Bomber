from __future__ import annotations

import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any

from utils.paths import LOGS_DIR
from utils.version import APP_NAME


def setup_logger(cfg: dict[str, Any]) -> logging.Logger:
    LOGS_DIR.mkdir(exist_ok=True)
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(getattr(logging, cfg["logging"]["level"].upper(), logging.INFO))
    logger.handlers.clear()
    logger.propagate = False

    if cfg["logging"]["enabled"]:
        stamp = datetime.now().strftime("%Y%m%d")
        handler = RotatingFileHandler(
            LOGS_DIR / f"chsmsbomber_{stamp}.log",
            maxBytes=int(cfg["logging"]["max_bytes"]),
            backupCount=int(cfg["logging"]["backup_count"]),
            encoding="utf-8",
        )
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s"
        ))
        logger.addHandler(handler)
    return logger


__all__ = ["setup_logger"]