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
