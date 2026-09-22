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
