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
        if not path:
            self.lines = ["(no log files yet)"]
            self._path = None
            return
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception as exc:
            raw = [f"(failed to read {path.name}: {exc})"]
        self._path = path
        self.lines = raw[-2000:] if raw else ["(empty log)"]
        self._last_mtime = path.stat().st_mtime
        # jump to bottom on first load
        self.cursor = max(0, len(self.lines) - 1)
        self.top = max(0, len(self.lines) - self.page_size)


    def render(self) -> Panel:
        # auto-reload if file changed and user hasn't scrolled up
        path = self._latest_log()
        at_bottom = self.cursor >= len(self.lines) - 2
        if path and path.stat().st_mtime != self._last_mtime and at_bottom:
            self._load()

        if self.cursor < self.top:
            self.top = self.cursor
        elif self.cursor >= self.top + self.page_size:
            self.top = self.cursor - self.page_size + 1

        body = Text()
        for i in range(self.top, min(self.top + self.page_size, len(self.lines))):
            line = self.lines[i]
            focused = i == self.cursor
            style = FG
            for level, lstyle in _LEVEL_STYLE.items():
                if f"[{level}]" in line:
                    style = lstyle
                    break
            marker = "▌" if focused else " "
            body.append(f"{marker} ", style=f"bold {PRIMARY}")
            body.append(line + "\n", style=style)

        head = Text()
        head.append("  file: ", style=FG_MUTED)
        head.append(str(self._path.name) if self._path else "(none)", style=ACCENT)
        head.append(f"   lines: {len(self.lines)}", style=FG_MUTED)
        head.append(f"   view: {self.top + 1}-"
                    f"{min(self.top + self.page_size, len(self.lines))}",
                    style=FG_MUTED)

        foot = Text()
        foot.append("\n  ", style=FG_MUTED)
        foot.append("↑ ↓", style=f"bold {OK}")
        foot.append(" scroll   ", style=FG_DIM)
        foot.append("r", style=f"bold {OK}")
        foot.append(" reload   ", style=FG_DIM)
        foot.append("Esc", style=f"bold {OK}")
        foot.append(" back", style=FG_DIM)

        return Panel(
