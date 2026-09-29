from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.attacker import STRATEGIES
from core.config import save_config
from ui.theme import (
    PRIMARY, ACCENT, OK, WARN, BAD,
    FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
)
from ui.tui import (
    Screen, KEY_UP, KEY_DOWN, KEY_ENTER, KEY_ESC, KEY_SPACE,
    KEY_LEFT, KEY_RIGHT,
)
from ui.widgets import Field


def _build_fields(cfg: dict) -> list[Field]:
    A, N, U, H, O, L = (
        cfg["attack"], cfg["network"], cfg["user_agent"],
        cfg["api_health"], cfg["output"], cfg["logging"],
    )
    return [
        Field("section", "ATTACK", "action", None),
        Field("attack.strategy", "Strategy", "cycle", A["strategy"],
              choices=list(STRATEGIES.keys())),
        Field("attack.threads", "Threads", "int", A["threads"]),
        Field("attack.rounds", "Rounds", "int", A["rounds"], hint="0 = unlimited"),
        Field("attack.delay", "Delay (s)", "float", A["delay"]),
        Field("attack.jitter", "Jitter (s)", "float", A["jitter"]),
        Field("attack.round_cooldown", "Round cooldown", "float", A["round_cooldown"]),
        Field("attack.rate_limit_per_sec", "Rate cap (req/s)", "float", A["rate_limit_per_sec"]),
        Field("attack.dry_run", "Dry-run", "bool", A["dry_run"]),
        Field("section", "NETWORK", "action", None),
        Field("network.timeout", "Timeout (s)", "int", N["timeout"]),
        Field("network.retries", "Retries", "int", N["retries"]),
        Field("network.retry_backoff", "Backoff factor", "float", N["retry_backoff"]),
        Field("network.verify_ssl", "Verify SSL", "bool", N["verify_ssl"]),
        Field("network.proxy_enabled", "Proxy enabled", "bool", N["proxy_enabled"]),
        Field("section", "USER-AGENT", "action", None),
        Field("user_agent.rotate", "Rotate UA", "bool", U["rotate"]),
        Field("section", "API HEALTH", "action", None),
        Field("api_health.enabled", "Enabled", "bool", H["enabled"]),
        Field("api_health.failure_threshold", "Failure threshold", "int", H["failure_threshold"]),
        Field("api_health.cooldown_seconds", "Cooldown (s)", "int", H["cooldown_seconds"]),
        Field("section", "OUTPUT", "action", None),
