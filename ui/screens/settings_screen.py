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
        Field("output.save_report", "Save report", "bool", O["save_report"]),
        Field("output.report_format", "Format", "cycle", O["report_format"],
              choices=["json", "csv"]),
        Field("output.include_html", "Include HTML", "bool", O["include_html"]),
        Field("section", "LOGGING", "action", None),
        Field("logging.enabled", "Log to file", "bool", L["enabled"]),
        Field("logging.level", "Level", "cycle", L["level"],
              choices=["DEBUG", "INFO", "WARNING", "ERROR"]),
        Field("action.save", "Save settings", "action", None),
        Field("action.back", "Back", "action", None),
    ]


class SettingsScreen(Screen):
    name = "settings"
    title = "Settings"
    hotkeys = {"⏎": "edit", "space": "toggle", "←→": "change"}

    def __init__(self, app) -> None:
        super().__init__(app)
        self.fields = _build_fields(app.cfg)
        self.cursor = self._first_editable(0)
        self.editing = False
        self.top = 0
        self.page_size = 18

    def _first_editable(self, start: int) -> int:
        for i in range(start, len(self.fields)):
            if self.fields[i].key != "section":
                return i
        return start

    def _is_section(self, i: int) -> bool:
        return self.fields[i].key == "section"

    def render_cache_key(self):
        return (self.cursor, self.top, self.editing)

    def render(self) -> Panel:
        if self.cursor < self.top:
            self.top = self.cursor
        elif self.cursor >= self.top + self.page_size:
            self.top = self.cursor - self.page_size + 1

        body = Table.grid(padding=(0, 2))
        body.add_column(ratio=1)

        for i in range(self.top, min(self.top + self.page_size, len(self.fields))):
            f = self.fields[i]
            if self._is_section(i):
                body.add_row(Text(f"\n  ── {f.label} ──", style=f"bold {ACCENT}"))
                continue
            body.add_row(f.render(i == self.cursor))

        info = Text()
        info.append(
            f"\n  showing "
            f"{self.top + 1}-{min(self.top + self.page_size, len(self.fields))}"
            f" of {len(self.fields)}",
            style=FG_MUTED,
        )

        return Panel(
            Align.left(Group(body, info), vertical="top"),
            title=f"[bold {PRIMARY}]  Settings  [/]",
            border_style=BORDER, box=BOX_MAIN, padding=(1, 2),
        )

    def handle_key(self, key: str) -> Optional[str]:
        f = self.fields[self.cursor]

        if self.editing:
            if key == KEY_ESC:
                self.editing = False
