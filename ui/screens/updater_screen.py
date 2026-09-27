from __future__ import annotations

import threading
from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.api_updater import (
    DEFAULT_APIS_URL, DEFAULT_MANIFEST_URL,
    check_for_updates, download_apis,
)
from core.apis import load_apis
from ui.theme import (
    PRIMARY, OK, WARN, BAD, FG, FG_DIM, FG_MUTED, BORDER, BOX_MAIN,
)
from ui.tui import Screen, KEY_ENTER, KEY_ESC


class UpdaterScreen(Screen):
    name = "updates"
    title = "Check for Updates"
    hotkeys = {"⏎": "download", "r": "re-check"}
    show_spinner = True

    def __init__(self, app) -> None:
        super().__init__(app)
        self.state = "idle"
        self.info = None
        self.error: Optional[str] = None
        self.bytes_written = 0
        self.bytes_total = 0

    def on_enter(self) -> None:
        self._start_check()

    def _start_check(self) -> None:
        self.state = "checking"
        self.show_spinner = True
        self.error = None
        self.app.notify("contacting manifest…", style=WARN)

        def _worker() -> None:
            try:
                info = check_for_updates(DEFAULT_MANIFEST_URL, DEFAULT_APIS_URL)
                self.info = info
                self.state = "ready"
                self.show_spinner = False
                self.app.notify("check complete", style=OK)
            except Exception as exc:
                self.error = str(exc)
                self.state = "error"
                self.show_spinner = False
                self.app.notify(f"check failed: {exc}", style=BAD)

        threading.Thread(target=_worker, daemon=True).start()

    def render_cache_key(self):
        return (self.state, self.bytes_written)

    def render(self) -> Panel:
        if self.state == "checking":
            return self._panel([
                Text("\n  Checking for API updates…\n", style=f"bold {WARN}"),
                Text("  fetching manifest and apis.json\n", style=FG_MUTED),
            ], subtitle="please wait")

        if self.state == "error":
            return self._panel([
                Text("\n  Update check failed\n", style=f"bold {BAD}"),
                Text(f"  {self.error}\n", style=FG),
            ], subtitle="press r to retry, Esc to return")

        if self.state in ("ready", "downloading", "done") and self.info:
            info = self.info
            t = Table.grid(padding=(0, 2))
            t.add_column(style=FG_MUTED)
            t.add_column(style=FG)
            t.add_row("Local hash", info.local_hash[:16] or "(none)")
            t.add_row("Remote hash", info.remote_hash[:16])
            t.add_row("Local APIs", str(info.local_count))
            t.add_row("Remote APIs", str(info.remote_count))
            t.add_row("Remote version", info.remote_version)

            header = Text()
            if info.available:
                header.append("\n  Update available\n\n", style=f"bold {WARN}")
            else:
                header.append("\n  Already up to date\n\n", style=f"bold {OK}")

            if self.state == "downloading":
                pct = (
                    self.bytes_written / self.bytes_total * 100
                    if self.bytes_total else 0
                )
                bar_len = 40
                filled = int(bar_len * pct / 100)
                bar = Text("  ")
                bar.append("█" * filled, style=f"bold {OK}")
                bar.append("░" * (bar_len - filled), style=FG_MUTED)
                bar.append(f"  {pct:5.1f}%   ", style=FG)
                bar.append(
