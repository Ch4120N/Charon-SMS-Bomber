"""Config load / save / merge / migrate."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from utils.paths import CONFIG_PATH
from utils.version import APP_VERSION

DEFAULT_CONFIG: dict[str, Any] = {
    "version": APP_VERSION,
    "network": {
        "timeout": 5,
        "retries": 2,
        "retry_backoff": 1.6,
        "verify_ssl": False,
        "proxy_enabled": False,
        "proxy_pool": [],
    },
    "attack": {
        "threads": 10,
        "rounds": 0,
        "delay": 0.05,
        "jitter": 0.02,
        "strategy": "smart",
        "hard_max_rounds": 100,
        "round_cooldown": 1.0,
        "rate_limit_per_sec": 0,
        "dry_run": False,
        "api_filter_tags": [],
        "api_filter_enabled_only": True,
    },
    "user_agent": {
        "rotate": True,
        "custom": [],
    },
