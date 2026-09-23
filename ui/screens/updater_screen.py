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
