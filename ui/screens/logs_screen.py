"""Live log tail viewer."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from ui.theme import (
    PRIMARY, ACCENT, OK, WARN, BAD, FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
)
from ui.tui import Screen, KEY_UP, KEY_DOWN, KEY_ESC
from utils.paths import LOGS_DIR


_LEVEL_STYLE = {
    "DEBUG": FG_MUTED,
    "INFO": FG,
    "WARNING": WARN,
    "ERROR": BAD,
    "CRITICAL": f"bold {BAD}",
}


class LogsScreen(Screen):
    name = "logs"
    title = "Logs"
    hotkeys = {"r": "reload", "g/G": "jump"}

    def __init__(self, app) -> None:
        super().__init__(app)
        self.lines: list[str] = []
        self.cursor = 0
        self.top = 0
        self.page_size = 24
        self._last_mtime = 0.0
        self._path: Optional[Path] = None

    def on_enter(self) -> None:
        self._load()

    def render_cache_key(self):
        return (self.cursor, self.top, len(self.lines))

    def _latest_log(self) -> Optional[Path]:
        if not LOGS_DIR.exists():
            return None
        files = sorted(LOGS_DIR.glob("*.log"), key=lambda p: p.stat().st_mtime)
        return files[-1] if files else None

    def _load(self) -> None:
        path = self._latest_log()
