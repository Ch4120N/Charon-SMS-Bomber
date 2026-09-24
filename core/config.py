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
    "api_health": {
        "enabled": True,
        "failure_threshold": 5,
        "cooldown_seconds": 60,
    },
    "ui": {
        "refresh_per_second": 30,
        "idle_refresh_per_second": 4,
        "idle_after_seconds": 1.5,
        "show_banner": True,
    },
    "logging": {
        "enabled": True,
        "level": "INFO",
        "max_bytes": 5242880,
        "backup_count": 3,
    },
    "output": {
        "save_report": True,
        "report_format": "json",
        "include_html": True,
    },
}


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _migrate(cfg: dict[str, Any]) -> dict[str, Any]:
    merged = _deep_merge(DEFAULT_CONFIG, cfg)
    if merged["attack"].get("strategy") not in (
        "smart", "unlimited", "round-robin", "random"
